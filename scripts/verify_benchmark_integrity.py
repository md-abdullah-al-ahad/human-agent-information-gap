#!/usr/bin/env python3
"""
Benchmark Self-Evaluation & Cryptographic Integrity Verifier.
Iterates through all entries in data/stage-4/manifest.json, re-computing SHA-256
hashes, checking file existence, and verifying dimensional integrity.
"""

import os
import json
import hashlib
import struct
import sys

MANIFEST_PATH = "data/stage-4/manifest.json"

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(filepath):
    """Read PNG IHDR dimensions without optional image packages."""
    with open(filepath, "rb") as image:
        header = image.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG with an IHDR header: {filepath}")
    return struct.unpack(">II", header[16:24])

def verify_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"[FAIL] Manifest not found at {MANIFEST_PATH}")
        return False

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    sites = data.get("sites", {})
    print(f"=== BENCHMARK SELF-EVALUATION INTEGRITY AUDIT ===")
    print(f"Total Registered Sites: {len(sites)}\n")

    all_passed = True

    for site_id, info in sites.items():
        name = info.get("name", "Unknown")
        print(f"Auditing Site {site_id}: {name}")
        site_passed = True
        if info.get("capture_status"):
            print(f"  Capture status: {info['capture_status']} (content usability is separate from file integrity)")

        # Check Screenshot
        ss_info = info.get("screenshot", {})
        ss_path = ss_info.get("path")
        expected_ss_sha = ss_info.get("sha256")

        if not os.path.exists(ss_path):
            print(f"  [FAIL] Screenshot missing: {ss_path}")
            all_passed = False
            continue

        actual_ss_sha = compute_sha256(ss_path)
        if actual_ss_sha != expected_ss_sha:
            print(f"  [FAIL] Screenshot SHA mismatch! Expected {expected_ss_sha}, got {actual_ss_sha}")
            all_passed = False
            site_passed = False
        else:
            print(f"  [PASS] Screenshot SHA-256 Verified: {actual_ss_sha[:16]}...")

        # Verify image opens and dimensions match
        try:
            width, height = png_dimensions(ss_path)
            dims_str = f"{width} x {height} px"
            if dims_str != ss_info.get("dimensions"):
                print(f"  [FAIL] Dimension mismatch: Expected {ss_info.get('dimensions')}, got {dims_str}")
                all_passed = False
                site_passed = False
            else:
                print(f"  [PASS] Dimensions Verified: {dims_str}")
        except ValueError as exc:
            print(f"  [FAIL] {exc}")
            all_passed = False
            site_passed = False

        # Check DOM
        dom_info = info.get("raw_dom", {})
        dom_path = dom_info.get("path")
        expected_dom_sha = dom_info.get("sha256")

        if not os.path.exists(dom_path):
            print(f"  [FAIL] DOM file missing: {dom_path}")
            all_passed = False
            continue

        actual_dom_sha = compute_sha256(dom_path)
        if actual_dom_sha != expected_dom_sha:
            print(f"  [FAIL] DOM SHA mismatch! Expected {expected_dom_sha}, got {actual_dom_sha}")
            all_passed = False
            site_passed = False
        else:
            print(f"  [PASS] DOM SHA-256 Verified: {actual_dom_sha[:16]}... ({os.path.getsize(dom_path):,} bytes)")

        print(f"  Status: {'FILE INTEGRITY VERIFIED' if site_passed else 'FILE INTEGRITY FAILED'} for {site_id}\n")

    if all_passed:
        print(f"=== ALL {len(sites)} REGISTERED FILE PAIRS MATCH THEIR HASHES AND DIMENSIONS ===")
    else:
        print("=== VERIFICATION FAILED ON ONE OR MORE SITES ===")

    return all_passed

if __name__ == "__main__":
    success = verify_manifest()
    sys.exit(0 if success else 1)
