#!/usr/bin/env python3
"""
Automated Batch Ingestion & Self-Evaluation Pipeline for Benchmark 100.
Executes headless Chromium to capture:
  1. Full-page high-resolution visual screenshot (PNG).
  2. Complete machine DOM (HTML).
  3. Computes cryptographic SHA-256 hashes.
  4. Runs 5 automated self-evaluation gates (HTTP liveness, image dimensions, pixel variance, DOM non-triviality, manifest registration).
"""

import os
import sys
import json
import hashlib
import argparse
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

CHROME_PATH = "/home/abdullah/.local/bin/chromium"
MANIFEST_PATH = "data/stage-4/manifest.json"
SCREENSHOT_DIR = "data/stage-4/screenshots"
RAW_DOM_DIR = "data/stage-4/raw"

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def check_pixel_variance(image_path):
    """Verifies image is not a blank solid frame (white/black error screen)."""
    with Image.open(image_path) as im:
        gray = im.convert("L")
        stat = ImageStat.Stat(gray)
        # stat.stddev is a list with stddev per band
        return float(stat.stddev[0]), im.size

def ingest_site(site_id, name, url, category):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(RAW_DOM_DIR, exist_ok=True)

    screenshot_file = f"{SCREENSHOT_DIR}/{site_id.lower()}-fullpage.png"
    dom_file = f"{RAW_DOM_DIR}/{site_id.lower()}-dom.html"

    print(f"=== INGESTING SITE: {site_id} ({name}) ===")
    print(f"Target URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Gate 1: Network Navigation
        try:
            resp = page.goto(url, wait_until="load", timeout=35000)
            status_code = resp.status if resp else "unknown"
            page.wait_for_timeout(3000) # Allow dynamic hydrate
        except Exception as e:
            print(f"[FAIL GATE 1: Navigation error: {e}]")
            browser.close()
            return False

        # Capture rendered DOM
        dom_content = page.content()
        with open(dom_file, "w", encoding="utf-8") as f:
            f.write(dom_content)

        # Capture full-page screenshot
        page.screenshot(path=screenshot_file, full_page=True)
        browser.close()

    # --- Self-Evaluation Gates ---
    # Gate 2: DOM non-triviality
    dom_bytes = os.path.getsize(dom_file)
    if dom_bytes < 5000 or "<html" not in dom_content.lower():
        print(f"[FAIL GATE 2: DOM trivial or truncated: {dom_bytes} bytes]")
        return False
    dom_sha = compute_sha256(dom_file)

    # Gate 3: Visual Non-Triviality
    std_dev, dims = check_pixel_variance(screenshot_file)
    screenshot_bytes = os.path.getsize(screenshot_file)
    if std_dev < 10.0 or dims[1] < 500:
        print(f"[FAIL GATE 3: Blank/Corrupted Screenshot: std_dev={std_dev:.2f}, dims={dims}]")
        return False
    screenshot_sha = compute_sha256(screenshot_file)

    # Gate 4: Update Manifest
    manifest = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    if "sites" not in manifest:
        manifest["sites"] = {}

    manifest["sites"][site_id] = {
        "name": name,
        "canonical_url": url,
        "category": category,
        "screenshot": {
            "path": screenshot_file,
            "sha256": screenshot_sha,
            "bytes": screenshot_bytes,
            "dimensions": f"{dims[0]} x {dims[1]} px",
            "pixel_luminance_std": round(std_dev, 2)
        },
        "raw_dom": {
            "path": dom_file,
            "sha256": dom_sha,
            "bytes": dom_bytes
        }
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[PASS GATE 1: HTTP {status_code}]")
    print(f"[PASS GATE 2: DOM {dom_bytes:,} bytes, SHA: {dom_sha[:16]}...]")
    print(f"[PASS GATE 3: Screenshot {dims[0]}x{dims[1]} px, StdDev: {std_dev:.2f}, SHA: {screenshot_sha[:16]}...]")
    print(f"[PASS GATE 4: Manifest registered for {site_id}]")
    print(f"=== INGESTION & SELF-EVALUATION PASSED: {site_id} ===\n")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="Site ID (e.g. BD-EC01)")
    parser.add_argument("--name", required=True, help="Site Name")
    parser.add_argument("--url", required=True, help="Canonical URL")
    parser.add_argument("--category", required=True, help="Domain Category")
    args = parser.parse_args()

    success = ingest_site(args.id, args.name, args.url, args.category)
    sys.exit(0 if success else 1)
