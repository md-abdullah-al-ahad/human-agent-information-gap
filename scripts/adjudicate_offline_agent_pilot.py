"""Rebuild the frozen offline pilot score from saved traces and reviewed decisions.

The hand-reviewed decisions below apply the rubric in docs/offline-agent-pilot-protocol.md.
They are deliberately explicit; no fuzzy string matcher decides visual or Bengali cases.
"""

import gzip
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results/experiment-03/offline-agent-pilot-manifest.json"
RUN = ROOT / "results/experiment-03/offline-agent-pilot-run-20261021"

# Everything not listed here matched the frozen reference answer and carried
# a saved-source observation or image-crop citation. The disputed visual items
# below were additionally checked against their saved reference crops.
FAILURES = {
    "BD2-20": ("timeout", "no_answer", "The 180-second limit stopped the session before a final answer."),
    "BD-TR03-05": ("wrong", "contradicted", "The saved popup prints USBAIN10; the agent answered USBAIR10."),
    "BD-QC02-05": ("abstained", "contradicted", "The saved 7% coupon visibly prints PUJA7; the agent falsely described it as a 9% coupon."),
    "BD-GV01-07": ("partial", "partial", "The answer says to use the oil in a vegetable dish but omits the required instruction to strain it (ছেঁকে)."),
    "BD-ED01-19": ("wrong", "contradicted", "The saved testimonial says পূর্ণিমা লস্কর; the agent answered পূর্ণিমা লক্ষ্মী / Purnima Lakshmi."),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def final_json(parts: list[str]) -> dict | None:
    if not parts:
        return None
    text = parts[-1].strip()
    blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    for candidate in reversed(blocks + [text]):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    match = re.search(r'\{\s*"status"\s*:', text)
    if match:
        try:
            return json.JSONDecoder().raw_decode(text[match.start():])[0]
        except json.JSONDecodeError:
            pass
    return None


def trace_metrics(path: Path) -> dict:
    outer = nested = errors = other = payload_bytes = 0
    cost = 0.0
    tokens = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0, "cache_write": 0}
    called_tools = []
    for line in gzip.open(path, "rt", encoding="utf-8"):
        event = json.loads(line)
        part = event.get("part") or {}
        if event.get("type") == "tool_use":
            outer += 1
            state = part.get("state") or {}
            metadata = state.get("metadata") or {}
            calls = (metadata.get("metadata") or {}).get("toolCalls") or []
            for call in calls:
                nested += 1
                called_tools.append(call.get("tool"))
                errors += call.get("status") == "error"
                other += not str(call.get("tool", "")).startswith("lwa.")
            payload_bytes += len(str(state.get("output", "")).encode())
            payload_bytes += len(json.dumps(metadata, ensure_ascii=False).encode())
        elif event.get("type") == "step_finish":
            cost += part.get("cost") or 0
            usage = part.get("tokens") or {}
            for key in ("input", "output", "reasoning"):
                tokens[key] += usage.get(key) or 0
            cache = usage.get("cache") or {}
            tokens["cache_read"] += cache.get("read") or 0
            tokens["cache_write"] += cache.get("write") or 0
    return {
        "execute_calls": outer, "nested_tool_calls": nested,
        "nested_tool_errors": errors, "non_lwa_attempts": other,
        "tools": sorted(set(called_tools)),
        "serialized_tool_payload_bytes": payload_bytes,
        "opencode_reported_cost_usd": round(cost, 8),
        "opencode_reported_tokens": tokens,
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    spec = json.loads((RUN / "run-spec.json").read_text())
    assert sha256(MANIFEST) == json.loads((Path("/tmp/lwa-offline-agent-pilot-packet-20261021") / "tasks.json").read_text())["gold_manifest_sha256"]
    assert sha256(RUN / "opencode-config.json") == spec["config_sha256"]
    assert sha256(RUN / "packet-hashes.json") == spec["packet_hashes_sha256"]
    raw = [json.loads(line) for line in (RUN / "run-results.jsonl").read_text().splitlines()]
    by_id = {row["case_id"]: row for row in raw}
    assert len(raw) == len(by_id) == 22
    output = {"run_spec_sha256": sha256(RUN / "run-spec.json"), "scored": [], "diagnostics": []}
    for item in manifest["scored_cases"]:
        case_id = item["case_id"]
        run = by_id[case_id]
        parsed = final_json(run["text_parts"])
        if case_id in FAILURES:
            outcome, support, note = FAILURES[case_id]
        else:
            assert run["reason"] == "completed" and parsed and parsed.get("status") == "answered", case_id
            assert parsed.get("evidence"), case_id
            outcome, support, note = "exact", "source_linked", "Answer matches frozen reference and cites a saved observation or image crop."
        output["scored"].append({
            "case_id": case_id, "site": item["site"], "rubric": item["rubric"],
            "expected": item["expected"], "agent_status": (parsed or {}).get("status"),
            "agent_answer": (parsed or {}).get("answer"),
            "agent_evidence": (parsed or {}).get("evidence", []),
            "outcome": outcome, "exact_pass": outcome == "exact", "source_support": support,
            "adjudication_note": note, "run_reason": run["reason"],
            "wall_seconds": run["wall_seconds"], "session_ids": run["session_ids"],
            "trace": run["trace"], **trace_metrics(RUN / run["trace"]),
        })
    for item in manifest["diagnostic_controls"]:
        case_id = item["control_id"]
        run = by_id[case_id]
        parsed = final_json(run["text_parts"])
        passed = case_id == "BD-TR02-access" and run["reason"] == "completed" and "blocked" in str((parsed or {}).get("answer", ""))
        output["diagnostics"].append({
            "control_id": case_id, "expected_state": item["expected_state"],
            "agent_answer": (parsed or {}).get("answer"), "passed": passed,
            "run_reason": run["reason"], "wall_seconds": run["wall_seconds"],
            "session_ids": run["session_ids"], "trace": run["trace"],
            **trace_metrics(RUN / run["trace"]),
        })
    output["summary"] = {
        "exact": sum(x["exact_pass"] for x in output["scored"]),
        "scored_total": len(output["scored"]),
        "wrong": sum(x["outcome"] == "wrong" for x in output["scored"]),
        "partial": sum(x["outcome"] == "partial" for x in output["scored"]),
        "abstained": sum(x["outcome"] == "abstained" for x in output["scored"]),
        "timeout": sum(x["outcome"] == "timeout" for x in output["scored"]),
        "diagnostics_passed": sum(x["passed"] for x in output["diagnostics"]),
        "diagnostics_total": len(output["diagnostics"]),
        "nested_tool_calls_total": sum(x["nested_tool_calls"] for x in output["scored"] + output["diagnostics"]),
        "non_lwa_attempts_total": sum(x["non_lwa_attempts"] for x in output["scored"] + output["diagnostics"]),
        "opencode_reported_cost_usd": round(sum(x["opencode_reported_cost_usd"] for x in output["scored"] + output["diagnostics"]), 8),
    }
    assert max(x["nested_tool_calls"] for x in output["scored"] + output["diagnostics"]) <= spec["max_tool_calls_per_task"]
    target = RUN / "scored-results.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output["summary"], indent=2))


if __name__ == "__main__":
    main()
