"""Run the answer-free offline packet through fresh OpenCode MCP sessions.

This runner never opens the gold manifest. Score only after raw traces are saved.
"""

import argparse
import gzip
import hashlib
import json
import os
import select
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = Path("/tmp/lwa-offline-agent-pilot-packet-20261021")
DEFAULT_OUT = ROOT / "results/experiment-03/offline-agent-pilot-run-20261021"
MODEL = "openrouter/qwen/qwen3.8-27b"
AGENT_PROMPT = (
    "Answer questions about a saved web capture using only the LWA MCP tools. "
    "Call tools.lwa.inspect_web_evidence through execute with mode='snapshot' "
    "and the supplied absolute HTML and image paths. Never use live mode or a URL as the target. "
    "Inspect cited observations or image crops when needed. Treat OCR as tentative; "
    "do not infer words from image filenames or unrelated page text. "
    "If the capture cannot support an exact answer, abstain. "
    "Return one JSON object with keys status ('answered' or 'abstained'), answer, "
    "evidence (list of observation IDs or image SHA/bbox citations), and uncertainty. "
    "The question is about the supplied saved capture, not today's website."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet_manifest(packet: Path) -> dict:
    files = []
    for path in sorted(packet.rglob("*")):
        if path.is_file():
            files.append({"path": str(path.relative_to(packet)), "sha256": sha256(path), "bytes": path.stat().st_size})
    return {"root": str(packet.resolve()), "files": files}


def configuration(out: Path) -> dict:
    ocr = Path("/home/abdullah/.cache/lwa-web/ocr-runtime/usr")
    env = {"LWA_EVIDENCE_DIR": str(out / "captures")}
    if (ocr / "bin/tesseract").exists():
        env.update({
            "PATH": f"{ocr / 'bin'}:{os.environ.get('PATH', '')}",
            "LD_LIBRARY_PATH": str(ocr / "lib"),
            "TESSDATA_PREFIX": str(ocr / "share/tessdata"),
        })
    return {
        "$schema": "https://opencode.ai/config.json",
        "mcp": {"servers": {
            "playwright": {"type": "local", "command": ["/bin/false"], "disabled": True},
            "lwa": {
                "type": "local",
                "command": ["/home/abdullah/.local/bin/uv", "run", "--no-project", "--with", "fastmcp", "--with", "Pillow", "python", str(ROOT / "scripts/mcp_lite_extractor.py")],
                "disabled": False,
                "codemode": True,
                "timeout": {"startup": 30000, "catalog": 30000, "execution": 30000},
                "environment": env,
            },
        }},
        "permissions": [
            {"action": action, "resource": "*", "effect": "deny"}
            for action in (
                "read", "edit", "glob", "grep", "shell", "subagent", "skill",
                "question", "webfetch", "websearch", "external_directory",
                "browser", "opencode_list_mcp_resources",
                "opencode_read_mcp_resource",
            )
        ],
        "agent": {"pilot": {"mode": "primary", "model": MODEL, "temperature": 0, "steps": 20, "prompt": AGENT_PROMPT}},
    }


def task_prompt(packet: Path, task: dict, site: dict) -> str:
    html = packet / site["dom_path"]
    images = [str(packet / path) for path in site["image_paths"]]
    return (
        f"Case ID: {task['case_id']}\n"
        f"Question: {task['question']}\n"
        f"Saved HTML target: {html}\n"
        f"Saved image_paths: {json.dumps(images)}\n"
        "Use only the LWA MCP tools and cite the evidence you actually used."
    )


def run_case(packet: Path, out: Path, config: Path, task: dict, site: dict, wall_limit: int, call_limit: int) -> dict:
    case_id = task["case_id"]
    trace_path = out / "traces" / f"{case_id}.jsonl.gz"
    stderr_path = out / "traces" / f"{case_id}.stderr.txt"
    prompt = task_prompt(packet, task, site)
    env = os.environ.copy()
    env["OPENCODE_CONFIG"] = str(config)
    cmd = ["opencode", "run", "--standalone", "--agent", "pilot", "--model", MODEL,
           "--format", "json", "--title", f"LWA offline pilot {case_id}", prompt]
    start = time.monotonic()
    tool_calls = 0
    tools_seen = []
    session_ids = set()
    answer_text = []
    reason = "completed"
    with gzip.open(trace_path, "wt", encoding="utf-8") as trace, stderr_path.open("w", encoding="utf-8") as err:
        proc = subprocess.Popen(cmd, cwd=packet, env=env, stdout=subprocess.PIPE, stderr=err, text=True, bufsize=1)
        while True:
            remaining = wall_limit - (time.monotonic() - start)
            if remaining <= 0:
                reason = "wall_timeout"
                proc.kill()
                break
            ready, _, _ = select.select([proc.stdout], [], [], min(remaining, 1.0))
            if not ready:
                if proc.poll() is not None:
                    break
                continue
            line = proc.stdout.readline()
            if not line:
                break
            trace.write(line)
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("sessionID"):
                session_ids.add(event["sessionID"])
            part = event.get("part") or {}
            if event.get("type") == "tool_use" or part.get("type") == "tool":
                tool_calls += 1
                tools_seen.append(part.get("tool") or event.get("tool"))
                if tool_calls > call_limit:
                    reason = "tool_limit_exceeded"
                    proc.kill()
                    break
            if event.get("type") == "text" or part.get("type") == "text":
                answer_text.append(part.get("text") or event.get("text") or "")
        try:
            exit_code = proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            exit_code = proc.wait()
    return {
        "case_id": case_id, "site": task["site"], "diagnostic": task["diagnostic"],
        "reason": reason, "exit_code": exit_code, "wall_seconds": round(time.monotonic() - start, 3),
        "tool_calls": tool_calls, "tools_seen": tools_seen, "session_ids": sorted(session_ids),
        "text_parts": answer_text, "trace": str(trace_path.relative_to(out)),
        "stderr": str(stderr_path.relative_to(out)),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--only", nargs="*")
    args = p.parse_args()
    packet, out = args.packet_dir.resolve(), args.output_dir.resolve()
    tasks_doc = json.loads((packet / "tasks.json").read_text())
    if not tasks_doc.get("gold_withheld") or tasks_doc["mode"] != "snapshot":
        raise SystemExit("Invalid answer-free snapshot packet")
    out.mkdir(parents=True, exist_ok=True)
    (out / "traces").mkdir(exist_ok=True)
    manifest = packet_manifest(packet)
    (out / "packet-hashes.json").write_text(json.dumps(manifest, indent=2) + "\n")
    config = out / "opencode-config.json"
    config.write_text(json.dumps(configuration(out), indent=2) + "\n")
    spec = {
        "opencode_version": "v2.1.1", "model": MODEL, "agent_prompt": AGENT_PROMPT,
        "packet_tasks_sha256": sha256(packet / "tasks.json"),
        "packet_hashes_sha256": sha256(out / "packet-hashes.json"),
        "config_sha256": sha256(config),
        "max_tool_calls_per_task": tasks_doc["max_tool_calls_per_task"],
        "max_wall_seconds_per_task": tasks_doc["max_wall_seconds_per_task"],
        "ocr_runtime_enabled": "TESSDATA_PREFIX" in configuration(out)["mcp"]["servers"]["lwa"]["environment"],
    }
    (out / "run-spec.json").write_text(json.dumps(spec, indent=2) + "\n")
    results_path = out / "run-results.jsonl"
    completed = {json.loads(line)["case_id"] for line in results_path.read_text().splitlines()} if results_path.exists() else set()
    for task in tasks_doc["tasks"]:
        if args.only is not None and task["case_id"] not in args.only:
            continue
        if task["case_id"] in completed:
            continue
        print(f"START {task['case_id']}", flush=True)
        result = run_case(packet, out, config, task, tasks_doc["sites"][task["site"]],
                          tasks_doc["max_wall_seconds_per_task"], tasks_doc["max_tool_calls_per_task"])
        with results_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(f"DONE {task['case_id']} {result['reason']} calls={result['tool_calls']} seconds={result['wall_seconds']}", flush=True)


if __name__ == "__main__":
    main()
