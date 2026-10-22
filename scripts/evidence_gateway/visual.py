"""Bounded, cached OCR and optional provider-neutral vision subprocess adapter."""

from __future__ import annotations

import base64
import csv
import io
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .compiler import crop_pixels, norm, terms
from .store import digest, encode


def runtime_identity():
    binary = os.environ.get("LWA_V2_TESSERACT") or shutil.which("tesseract")
    languages = os.environ.get("LWA_V2_OCR_LANG", "eng+ben")
    runtime = {
        "tesseract": None,
        "languages": languages,
        "traineddata": {},
        "vision_id": os.environ.get("LWA_V2_VISION_ID"),
        "vision_command_sha256": digest(
            os.environ.get("LWA_V2_VISION_COMMAND", "").encode()
        ),
    }
    if binary:
        path = Path(binary)
        if path.is_file():
            runtime["tesseract"] = {
                "path": str(path.resolve()),
                "sha256": digest(path.read_bytes()),
            }
        tessdata = os.environ.get("TESSDATA_PREFIX")
        if tessdata:
            for language in languages.split("+"):
                candidate = Path(tessdata) / (language + ".traineddata")
                if candidate.is_file():
                    runtime["traineddata"][language] = digest(candidate.read_bytes())
    return runtime


def read_ocr(store, region, runtime, psm, timeout):
    key = "ocr:" + digest(
        encode([region["source_sha256"], region["bbox"], runtime, psm, "ocr-1"])
    )
    cached = store.cached(key)
    if cached is not None:
        return cached, True
    if not runtime["tesseract"]:
        return {"blocks": [], "error": "ocr_unavailable"}, False
    from PIL import Image, ImageOps

    pixels, dimensions = crop_pixels(store, region, max_pixels=1_500_000)
    with Image.open(io.BytesIO(pixels)) as opened:
        image = ImageOps.grayscale(opened)
        # Two layout modes are corroborating readings of one engine, not independent truth.
        if psm == 6 and image.width * image.height <= 375000:
            image = image.resize((image.width * 2, image.height * 2))
        dimensions = image.size
        with tempfile.TemporaryDirectory(prefix="lwa-v2-ocr-") as folder:
            path = Path(folder) / "region.png"
            image.save(path)
            try:
                process = subprocess.run(
                    [
                        runtime["tesseract"]["path"],
                        str(path),
                        "stdout",
                        "-l",
                        runtime["languages"],
                        "--psm",
                        str(psm),
                        "tsv",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return {"blocks": [], "error": "ocr_budget_exhausted"}, False
    if process.returncode:
        return {
            "blocks": [],
            "error": "ocr_failed",
            "detail": process.stderr[-240:],
        }, False
    blocks = {}
    box = region["bbox"]
    sx, sy = (box[2] - box[0]) / dimensions[0], (box[3] - box[1]) / dimensions[1]
    for word in csv.DictReader(io.StringIO(process.stdout), delimiter="\t"):
        text = word.get("text", "").strip()
        if not text or word.get("level") != "5":
            continue
        try:
            confidence = float(word["conf"])
            x, y, w, h = [int(word[k]) for k in ("left", "top", "width", "height")]
        except (ValueError, KeyError):
            continue
        group = (word["block_num"], word["par_num"])
        item = blocks.setdefault(
            group,
            {"words": [], "confidences": [], "bbox": [box[2], box[3], box[0], box[1]]},
        )
        item["words"].append(text)
        item["confidences"].append(confidence)
        b = item["bbox"]
        item["bbox"] = [
            min(b[0], int(box[0] + x * sx)),
            min(b[1], int(box[1] + y * sy)),
            max(b[2], min(box[2], int(box[0] + (x + w) * sx) + 1)),
            max(b[3], min(box[3], int(box[1] + (y + h) * sy) + 1)),
        ]
    result = {
        "blocks": [
            {
                "text": norm(" ".join(b["words"])),
                "bbox": b["bbox"],
                "min_confidence": min(b["confidences"]),
                "mean_confidence": round(
                    sum(b["confidences"]) / len(b["confidences"]), 2
                ),
            }
            for b in blocks.values()
        ],
        "error": None,
    }
    return store.cache(key, result), False


def read_vision(store, region, runtime, timeout):
    configured = os.environ.get("LWA_V2_VISION_COMMAND")
    if not configured or not runtime["vision_id"]:
        return {"blocks": [], "error": "vision_unconfigured"}, False
    key = "vision:" + digest(
        encode([region["source_sha256"], region["bbox"], runtime, "vision-1"])
    )
    cached = store.cached(key)
    if cached is not None:
        return cached, True
    command = json.loads(configured)
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(v, str) for v in command)
    ):
        raise ValueError("LWA_V2_VISION_COMMAND must be a JSON argv array")
    pixels, _ = crop_pixels(store, region)
    request = {
        "image_png_base64": base64.b64encode(pixels).decode(),
        "instruction": "Transcribe the text exactly, preserving script and reading order. Do not guess unclear characters.",
        "model_id": runtime["vision_id"],
    }
    with tempfile.TemporaryFile() as output:
        try:
            process = subprocess.run(
                command,
                input=encode(request),
                stdout=output,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"blocks": [], "error": "vision_budget_exhausted"}, False
        output.seek(0)
        raw = output.read(32001)
    if process.returncode or len(raw) > 32000:
        return {"blocks": [], "error": "vision_failed"}, False
    data = json.loads(raw)
    if data.get("model_id") != runtime["vision_id"] or not isinstance(
        data.get("text"), str
    ):
        raise ValueError("vision adapter must return text and the configured model_id")
    result = {
        "blocks": [
            {
                "text": data["text"][:4000],
                "bbox": region["bbox"],
                "min_confidence": None,
            }
        ],
        "usage": data.get("usage"),
        "model_id": data["model_id"],
        "error": None,
    }
    return store.cache(key, result), False


def visual_evidence(store, index, query, runtime, remaining_seconds):
    """Select regions, use an overview for orientation, and retain each reading separately."""
    budget = query["budget"]
    regions = [r for r in index["records"] if r["source_kind"] == "image_region"]
    usage = {
        "ocr_calls": 0,
        "ocr_cache_hits": 0,
        "vision_calls": 0,
        "vision_cache_hits": 0,
        "vision_usage": [],
    }

    def count(kind, reading, hit):
        if hit:
            usage[kind + "_cache_hits"] += 1
        elif reading["error"] not in {"ocr_unavailable", "vision_unconfigured"}:
            usage[kind + "_calls"] += 1

    failures, output = [], []
    wanted = terms(
        query["question"]
        + " "
        + query["subject"]
        + " "
        + " ".join(query["qualifiers"].values())
    )
    preferred = set(query["evidence_ids"])
    selected = sorted(
        regions,
        key=lambda r: (
            -int(r["id"] in preferred),
            -len(wanted & terms(r["anchor"])),
            r["order"],
            r["id"],
        ),
    )
    # Historical screenshots have no DOM-to-pixel mapping. One cached OCR overview
    # can locate a heading before we spend the remaining budget on detailed regions.
    if (
        selected
        and not preferred
        and not any(r["anchor"] for r in selected)
        and runtime["tesseract"]
        and budget["max_ocr_calls"]
    ):
        manifest = store.get(index["capture_id"], "capture")
        for image in manifest["images"][:1]:
            if image["width"] * image["height"] > 1_000_000:
                overview = dict(
                    selected[0],
                    source_sha256=image["sha256"],
                    bbox=[0, 0, image["width"], image["height"]],
                )
                reading, hit = read_ocr(
                    store, overview, runtime, 11, max(0.1, remaining_seconds())
                )
                count("ocr", reading, hit)
                hits = [b for b in reading["blocks"] if wanted & terms(b["text"])]

                def overlap(r, blocks=hits, image_sha=image["sha256"]):
                    return sum(
                        len(wanted & terms(b["text"]))
                        for b in blocks
                        if r["source_sha256"] == image_sha
                        and r["bbox"][0]
                        <= (b["bbox"][0] + b["bbox"][2]) / 2
                        <= r["bbox"][2]
                        and r["bbox"][1]
                        <= (b["bbox"][1] + b["bbox"][3]) / 2
                        <= r["bbox"][3]
                    )

                selected.sort(key=lambda r: (-overlap(r), r["order"], r["id"]))
                if reading["error"]:
                    failures.append(reading["error"])
    selected = selected[: budget["max_visual_regions"]]
    attempts = usage["ocr_calls"] + usage["ocr_cache_hits"]
    for region in selected:
        for psm in (11, 6):
            if attempts >= budget["max_ocr_calls"] or remaining_seconds() < 0.2:
                break
            attempts += 1
            reading, hit = read_ocr(
                store, region, runtime, psm, max(0.1, remaining_seconds())
            )
            count("ocr", reading, hit)
            if reading["error"]:
                failures.append(reading["error"])
            for block in reading["blocks"]:
                evidence = {
                    "capture_id": index["capture_id"],
                    "source_kind": "visual_reading",
                    "source_sha256": region["source_sha256"],
                    "region_id": region["id"],
                    "bbox": block["bbox"],
                    "text": block["text"],
                    "anchor": region["anchor"],
                    "binding": region["binding"],
                    "method": f"tesseract-psm-{psm}",
                    "runtime": runtime,
                    "min_confidence": block["min_confidence"],
                    "human_visibility": "saved_pixels",
                    "order": region["order"],
                }
                output.append(dict(evidence, id=store.put("ev", evidence)))
    if selected and budget["max_vision_calls"] and remaining_seconds() > 0.2:
        region = selected[0]
        reading, hit = read_vision(
            store, region, runtime, max(0.1, remaining_seconds())
        )
        count("vision", reading, hit)
        if reading["error"]:
            failures.append(reading["error"])
        if reading.get("usage") is not None:
            usage["vision_usage"].append(reading["usage"])
        for block in reading["blocks"]:
            evidence = {
                "capture_id": index["capture_id"],
                "source_kind": "visual_reading",
                "region_id": region["id"],
                "source_sha256": region["source_sha256"],
                "bbox": region["bbox"],
                "text": block["text"],
                "anchor": region["anchor"],
                "binding": region["binding"],
                "method": "vision:" + runtime["vision_id"],
                "runtime": runtime,
                "human_visibility": "saved_pixels",
                "order": region["order"],
            }
            output.append(dict(evidence, id=store.put("ev", evidence)))
    return output, selected, sorted(set(failures)), usage
