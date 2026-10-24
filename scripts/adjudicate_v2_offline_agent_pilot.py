"""Export a completed v2 pilot for review, or rebuild its reviewed score.

No inherited v1 pass/fail decisions are used. The first pass writes a review
packet; --finalize requires an explicit decision for every scored/control item.
"""

import argparse
import json
import sqlite3
from pathlib import Path

from adjudicate_offline_agent_pilot import final_json, trace_metrics
from run_offline_agent_pilot import ROOT, sha256


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    run = args.run_dir.resolve()
    rows = [
        json.loads(line)
        for line in (run / "run-results.jsonl").read_text().splitlines()
    ]
    assert len(rows) == len({r["case_id"] for r in rows}) == 22, (
        "Wait for all frozen tasks"
    )
    spec = json.loads((run / "run-spec.json").read_text())
    for file, expected in spec["code_hashes"].items():
        assert sha256(ROOT / file) == expected
    for case_id, expected in spec["config_hashes"].items():
        assert sha256(run / "configs" / f"{case_id}.json") == expected
    gold_path = ROOT / "results/experiment-03/offline-agent-pilot-manifest.json"
    packet_hashes = json.loads((run / "packet-hashes.json").read_text())
    packet_tasks = json.loads((Path(packet_hashes["root"]) / "tasks.json").read_text())
    assert sha256(gold_path) == packet_tasks["gold_manifest_sha256"]
    gold = json.loads(gold_path.read_text())
    references = {r["case_id"]: r for r in gold["scored_cases"]}
    references.update({r["control_id"]: r for r in gold["diagnostic_controls"]})
    reviews, audits = [], {}
    for row in rows:
        case_id = row["case_id"]
        with sqlite3.connect(run / "captures" / case_id / "store.sqlite3") as db:
            events = [
                {"at": at, "operation": op, "data": json.loads(data)}
                for at, op, data in db.execute(
                    "SELECT at,operation,data FROM audit ORDER BY rowid"
                )
            ]
            certificates = {
                f"cert:{key}": json.loads(data)
                for key, data in db.execute(
                    "SELECT id,data FROM records WHERE kind='cert'"
                )
            }
            sessions = [
                dict(zip(("id", "calls", "image_pixels"), s, strict=True))
                for s in db.execute("SELECT id,calls,image_pixels FROM sessions")
            ]
            parsed = final_json(row["text_parts"])
            citation_validity = {}
            for evidence_id in (parsed or {}).get("evidence", []):
                if not isinstance(evidence_id, str) or ":" not in evidence_id:
                    citation_validity[str(evidence_id)] = False
                    continue
                kind, key = evidence_id.split(":", 1)
                citation_validity[evidence_id] = bool(
                    db.execute(
                        "SELECT 1 FROM records WHERE kind=? AND id=?", (kind, key)
                    ).fetchone()
                )
        audits[case_id] = {
            "events": events,
            "certificates": certificates,
            "sessions": sessions,
        }
        assert all(s["calls"] <= 20 for s in sessions)
        gate_events = [e["data"] for e in events if e["operation"] == "verify"]
        accepted = [e for e in gate_events if e["status"] == "accepted"]
        reviews.append(
            {
                "case_id": case_id,
                "site": row["site"],
                "diagnostic": row["diagnostic"],
                "reference": references[case_id],
                "agent_final": parsed,
                "final_text": row["text_parts"][-1] if row["text_parts"] else None,
                "reason": row["reason"],
                "exit_code": row["exit_code"],
                "wall_seconds": row["wall_seconds"],
                "session_ids": row["session_ids"],
                "trace": row["trace"],
                "trace_sha256": sha256(run / row["trace"]),
                "citation_handles_exist": citation_validity,
                "gate_events": gate_events,
                "final_answer_literal_matches_an_accepted_value": any(
                    (parsed or {}).get("answer") == event["answer"]["value"]
                    for event in accepted
                ),
                "session_counters": sessions,
                **trace_metrics(run / row["trace"]),
            }
        )
    save(run / "gateway-audit.json", audits)
    save(run / "review-packet.json", reviews)
    if not args.finalize:
        print(f"Exported {len(reviews)} cases for explicit review; no score assigned.")
        return
    decisions = json.loads((run / "adjudication.json").read_text())
    assert set(decisions) == set(references), (
        "Every case needs an explicit reviewed decision"
    )
    output = {
        "run_spec_sha256": sha256(run / "run-spec.json"),
        "adjudication_sha256": sha256(run / "adjudication.json"),
        "scored": [],
        "diagnostics": [],
    }
    for review in reviews:
        decision = decisions[review["case_id"]]
        assert decision.get("note"), "Review must explain the decision"
        record = {**review, "adjudication": decision}
        if review["diagnostic"]:
            assert type(decision["passed"]) is bool
            output["diagnostics"].append(record)
        else:
            assert decision["outcome"] in {
                "exact",
                "wrong",
                "partial",
                "abstained",
                "timeout",
                "error",
            }
            record["exact_pass"] = decision["outcome"] == "exact"
            if record["exact_pass"]:
                assert review["agent_final"]["status"] == "answered"
                assert decision["source_support"] in {"source_linked", "ungrounded"}
            output["scored"].append(record)
    summary = {
        outcome: sum(r["adjudication"]["outcome"] == outcome for r in output["scored"])
        for outcome in ("exact", "wrong", "partial", "abstained", "timeout", "error")
    }
    summary.update(
        {
            "scored_total": len(output["scored"]),
            "diagnostics_passed": sum(
                r["adjudication"]["passed"] for r in output["diagnostics"]
            ),
            "diagnostics_total": len(output["diagnostics"]),
        }
    )
    for group in ("scored", "diagnostics"):
        subset = output[group]
        summary[group + "_metrics"] = {
            "wall_seconds": round(sum(r["wall_seconds"] for r in subset), 3),
            "nested_tool_calls": sum(r["nested_tool_calls"] for r in subset),
            "opencode_reported_cost_usd": round(
                sum(r["opencode_reported_cost_usd"] for r in subset), 8
            ),
            "opencode_reported_tokens": {
                key: sum(r["opencode_reported_tokens"][key] for r in subset)
                for key in ("input", "output", "reasoning", "cache_read", "cache_write")
            },
        }
    output["summary"] = summary
    save(run / "scored-results.json", output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
