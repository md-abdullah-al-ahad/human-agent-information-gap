"""Run the frozen answer-free pilot packet against the unmodified v2 gateway.

Gold is not opened here. Every task gets a fresh agent and source store. Score
only after all traces have been saved. The shipped visual gate stays enabled.
"""

import argparse
import gzip
import json
import os
import selectors
import signal
import subprocess
import time
from pathlib import Path

from evidence_gateway.store import Store
from run_offline_agent_pilot import MODEL, ROOT, configuration, packet_manifest, sha256

PROMPT = (
    "Answer questions about a saved web capture using only the LWA v2 MCP tools. "
    "Call tools through execute using JavaScript (e.g. const res = await tools.lwa.resolve_evidence({ request: { source: { kind: 'snapshot', id: '...' }, answer_type: '...', subject: '...', field: '...', question: '...' } }); return res;). "
    "Choose the answer_type, subject (an exact source entity/container label), field, "
    "qualifiers and optional position appropriate to the question. You may inspect "
    "returned evidence IDs using await tools.lwa.inspect_evidence({ evidence_id: '...', view: 'crop' or 'text' }), and "
    "refine requests within the budget. Do not use file, shell, fetch, live-web, "
    "other tools, filenames, or outside knowledge as answer evidence. "
    "The question concerns the supplied capture, not today's website. Treat OCR "
    "as tentative and unresolved searches as incomplete coverage, not global absence. "
    "For a factual answer, call await tools.lwa.verify_answer({ certificate_id: '...', proposed_answer: { value: '...', evidence_ids: [...] } }). "
    "Only return status='answered' for a value accepted by verify_answer. "
    "For numbers and statistics, resolve with the container subject or field, or inspect text; submit the extracted value to verify_answer. "
    "If a subject or value is not observed after inspecting 1-2 evidence records, STOP SEARCHING IMMEDIATELY; "
    "do not enter repeated retry loops; promptly return status='abstained' with certificate diagnostics. "
    "For access-state or unresolved-reference diagnostics you may report the explicit "
    "certificate status and its limitations, citing the certificate. "
    "Return one JSON object with keys status ('answered' or 'abstained'), answer, "
    "evidence (list of IDs), certificate_id, verification_status, and uncertainty. "
    "Keep the final answer concise; do not add unsupported claims."
)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def case_config(out, case_id):
    config = configuration(out)
    ocr = Path("/home/abdullah/.cache/lwa-web/ocr-runtime/usr")
    config["agent"]["pilot"]["prompt"] = PROMPT
    config["mcp"]["servers"]["lwa"].update(
        {
            "command": [
                str(ROOT / ".venv-lwa-v2/bin/python"),
                str(ROOT / "scripts/mcp_evidence_gateway.py"),
            ],
            "environment": {
                "LWA_V2_STORE": str(out / "captures" / case_id),
                "LWA_V2_SESSION_ID": case_id,
                "LWA_V2_MAX_CALLS": "20",
                "LWA_V2_ALLOW_LIVE": "0",
                "LWA_V2_ALLOW_VISUAL_ANSWERS": "1",
                "LWA_V2_TESSERACT": str(ocr / "bin/tesseract"),
                "LD_LIBRARY_PATH": str(ocr / "lib"),
                "TESSDATA_PREFIX": str(ocr / "share/tessdata"),
                "PYTHONPATH": str(ROOT / "scripts"),
            },
        }
    )
    return config


def run_case(packet, out, task, snapshot, wall_limit, model=MODEL):
    case_id = task["case_id"]
    config = out / "configs" / f"{case_id}.json"
    trace_path = out / "traces" / f"{case_id}.jsonl.gz"
    stderr_path = out / "traces" / f"{case_id}.stderr.txt"
    prompt = (
        f"Case ID: {case_id}\nQuestion: {task['question']}\n"
        f"Snapshot source: {json.dumps({'kind': 'snapshot', 'id': snapshot['snapshot_id']})}\n"
        "Use only the three LWA v2 tools. Answer only if the final gate accepts it; "
        "otherwise report an abstention and the limitation."
    )
    env = os.environ.copy()
    # Avoid inherited optional adapters/policy overrides changing this frozen run.
    for key in list(env):
        if key.startswith("LWA_V2_"):
            del env[key]
    env["OPENCODE_CONFIG"] = str(config)
    command = [
        "opencode",
        "run",
        "--standalone",
        "--agent",
        "pilot",
        "--model",
        model,
        "--format",
        "json",
        "--title",
        f"LWA v2 pilot {case_id}",
        prompt,
    ]
    start = time.monotonic()
    reason, sessions, answers, tools = "completed", set(), [], []
    with (
        gzip.open(trace_path, "wt", encoding="utf-8") as trace,
        stderr_path.open("w") as err,
    ):
        proc = subprocess.Popen(
            command,
            cwd=packet,
            env=env,
            stdout=subprocess.PIPE,
            stderr=err,
            start_new_session=True,
        )
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)
        pending = b""

        def consume(line):
            text = line.decode("utf-8", errors="replace")
            trace.write(text + "\n")
            trace.flush()
            try:
                event = json.loads(text)
            except json.JSONDecodeError:
                return
            if event.get("sessionID"):
                sessions.add(event["sessionID"])
            part = event.get("part") or {}
            if event.get("type") == "tool_use":
                tools.append(part.get("tool"))
            if event.get("type") == "text":
                answers.append(part.get("text") or event.get("text") or "")

        try:
            while True:
                remaining = wall_limit - (time.monotonic() - start)
                if remaining <= 0:
                    reason = "wall_timeout"
                    break
                if not selector.select(min(remaining, 1)):
                    continue
                chunk = os.read(proc.stdout.fileno(), 65536)
                if not chunk:
                    break
                pending += chunk
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    consume(line)
            if pending:
                consume(pending)
        finally:
            selector.close()
            # Also terminate MCP/browser/OCR descendants if the agent times out.
            if reason == "wall_timeout" or proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            exit_code = proc.wait(timeout=10)
    return {
        "case_id": case_id,
        "site": task["site"],
        "diagnostic": task["diagnostic"],
        "reason": reason,
        "exit_code": exit_code,
        "wall_seconds": round(time.monotonic() - start, 3),
        "tool_calls": len(tools),
        "tools_seen": tools,
        "session_ids": sorted(sessions),
        "text_parts": answers,
        "trace": str(trace_path.relative_to(out)),
        "stderr": str(stderr_path.relative_to(out)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--packet-dir",
        type=Path,
        default=Path("/tmp/lwa-offline-agent-pilot-packet-20261021"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="ollama/qwen2.5-coder:3b")
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    packet, out = args.packet_dir.resolve(), args.output_dir.resolve()
    tasks = json.loads((packet / "tasks.json").read_text())
    assert tasks["gold_withheld"] and tasks["mode"] == "snapshot"
    if not (out / "run-spec.json").exists():
        for sub in ("traces", "configs", "captures"):
            (out / sub).mkdir(parents=True, exist_ok=True)
        current = packet_manifest(packet)
        old = json.loads(
            (
                ROOT
                / "results/experiment-03/offline-agent-pilot-run-20261021/packet-hashes.json"
            ).read_text()
        )
        assert current["files"] == old["files"], "Pilot packet changed"
        save(out / "packet-hashes.json", current)
        snapshots = {}
        configs = {}
        for task in tasks["tasks"]:
            case_id = task["case_id"]
            site = tasks["sites"][task["site"]]
            snapshots[case_id] = Store(out / "captures" / case_id).register(
                packet,
                site["dom_path"],
                site["image_paths"],
                url=site["url_at_capture"],
            )
            target = out / "configs" / f"{case_id}.json"
            save(target, case_config(out, case_id))
            configs[case_id] = sha256(target)
        save(out / "snapshots.json", snapshots)
        sources = list((ROOT / "scripts/evidence_gateway").glob("*.py")) + [
            ROOT / "scripts/mcp_evidence_gateway.py",
            Path(__file__).resolve(),
        ]
        save(
            out / "run-spec.json",
            {
                "model": args.model,
                "opencode_version": subprocess.check_output(
                    ["opencode", "--version"], text=True
                ).strip(),
                "agent_prompt": PROMPT,
                "temperature": 0,
                "max_tool_calls_per_task": 20,
                "max_wall_seconds_per_task": 180,
                "gate_policy": "calibrated: grounded citations accepted, visual enabled",
                "ocr_runtime_enabled": True,
                "live_web_enabled": False,
                "fresh_store_per_task": True,
                "new_paid_vision_adapter": False,
                "packet_tasks_sha256": sha256(packet / "tasks.json"),
                "packet_hashes_sha256": sha256(out / "packet-hashes.json"),
                "snapshots_sha256": sha256(out / "snapshots.json"),
                "config_hashes": configs,
                "code_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in sources},
                "comparison": "same pilot packet and model ID; historical v1, not contemporaneous randomized baseline",
            },
        )
    spec = json.loads((out / "run-spec.json").read_text())
    for name, sha in spec["code_hashes"].items():
        assert sha256(ROOT / name) == sha, f"Code changed after freeze: {name}"
    assert sha256(out / "snapshots.json") == spec["snapshots_sha256"]
    assert (
        packet_manifest(packet)["files"]
        == json.loads((out / "packet-hashes.json").read_text())["files"]
    )
    snapshots = json.loads((out / "snapshots.json").read_text())
    results = out / "run-results.jsonl"
    completed = (
        {json.loads(line)["case_id"] for line in results.read_text().splitlines()}
        if results.exists()
        else set()
    )
    for task in tasks["tasks"]:
        case_id = task["case_id"]
        if case_id in completed or (args.only is not None and case_id not in args.only):
            continue
        assert (
            sha256(out / "configs" / f"{case_id}.json")
            == spec["config_hashes"][case_id]
        )
        print(f"START {case_id}", flush=True)
        result = run_case(packet, out, task, snapshots[case_id], 180, model=spec["model"])
        if result["exit_code"] != 0 and (out / result["trace"]).exists():
            try:
                with gzip.open(out / result["trace"], "rt", encoding="utf-8") as tf:
                    trace_content = tf.read()
                if "provider.quota" in trace_content or "RESOURCE_EXHAUSTED" in trace_content or "rate_limit" in trace_content:
                    print(f"QUOTA WAIT 55s then RETRY {case_id}...", flush=True)
                    time.sleep(55)
                    result = run_case(packet, out, task, snapshots[case_id], 180, model=spec["model"])
            except Exception:
                pass
        with results.open("a") as stream:
            stream.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(
            f"DONE {case_id} {result['reason']} calls={result['tool_calls']} seconds={result['wall_seconds']}",
            flush=True,
        )
        if "google/" in str(spec["model"]):
            time.sleep(30)


if __name__ == "__main__":
    main()
