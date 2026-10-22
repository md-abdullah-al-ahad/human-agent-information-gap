"""Verify the frozen saved-capture pilot and optionally build a gold-free packet.

This script does not invoke an agent, revisit a site, or score any answer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results/experiment-03/offline-agent-pilot-manifest.json"


def _verified_path(artifact: dict[str, str]) -> Path:
    relative = Path(artifact["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"pilot artifact must be repository-relative: {relative}")
    path = ROOT / relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != artifact["sha256"]:
        raise ValueError(f"pilot artifact hash mismatch: {relative}")
    return path


def verify_manifest() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "frozen_not_run":
        raise ValueError("pilot manifest must remain marked frozen_not_run before an agent trial")
    cases = manifest["scored_cases"]
    controls = manifest["diagnostic_controls"]
    if len(cases) != 20 or len(controls) != 2:
        raise ValueError("pilot requires exactly 20 scored cases and 2 diagnostics")
    ids = [case["case_id"] for case in cases] + [case["control_id"] for case in controls]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate pilot case/control ID")
    for site in manifest["source_sets"].values():
        _verified_path(site["dom"])
        _verified_path(site["screenshot"])
        for image in site["supplemental_images"]:
            _verified_path(image)
    for case in cases:
        if case["site"] not in manifest["source_sets"] or not case["question"] or not case["expected"]:
            raise ValueError(f"incomplete pilot case: {case.get('case_id')}")
        _verified_path(case["reference"])
    for control in controls:
        if control["site"] not in manifest["source_sets"] or control["scored_in_accuracy"]:
            raise ValueError(f"invalid diagnostic control: {control.get('control_id')}")
    return manifest


def build_packet(destination: Path, manifest: dict) -> None:
    if destination.exists():
        raise FileExistsError(f"packet destination already exists: {destination}")
    destination.mkdir(parents=True)
    sites = {}
    for key, source in manifest["source_sets"].items():
        folder = destination / "assets" / key
        folder.mkdir(parents=True)
        page = folder / "page.html"
        screenshot = folder / "screenshot.png"
        shutil.copy2(_verified_path(source["dom"]), page)
        shutil.copy2(_verified_path(source["screenshot"]), screenshot)
        images = [str(screenshot.relative_to(destination))]
        for index, image in enumerate(source["supplemental_images"], start=1):
            target = folder / f"supplemental-{index}.png"
            shutil.copy2(_verified_path(image), target)
            images.append(str(target.relative_to(destination)))
        sites[key] = {
            "url_at_capture": source["url"],
            "dom_path": str(page.relative_to(destination)),
            "image_paths": images,
            "note": "Saved snapshot only; these files do not establish current site state.",
        }
    tasks = [
        {"case_id": case["case_id"], "site": case["site"],
         "question": case["question"], "diagnostic": False}
        for case in manifest["scored_cases"]
    ] + [
        {"case_id": control["control_id"], "site": control["site"],
         "question": control["question"], "diagnostic": True}
        for control in manifest["diagnostic_controls"]
    ]
    packet = {
        "status": "prepared_not_run", "mode": "snapshot", "sites": sites, "tasks": tasks,
        "gold_withheld": True,
        "gold_manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "max_tool_calls_per_task": 20, "max_wall_seconds_per_task": 180,
    }
    (destination / "tasks.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-dir", type=Path, help="write a separate gold-free offline packet")
    args = parser.parse_args()
    manifest = verify_manifest()
    print(f"Verified {len(manifest['scored_cases'])} scored cases and "
          f"{len(manifest['diagnostic_controls'])} diagnostics against saved artifact hashes")
    if args.packet_dir:
        build_packet(args.packet_dir, manifest)
        print(f"Prepared gold-free packet at {args.packet_dir}; no agent run started")


if __name__ == "__main__":
    main()
