"""Local, content-addressed evidence records for the LWA-Web MCP tools.

The store is a cache of captures, not a ground-truth database. A capture handle
identifies one acquisition, and every observation is resolved within that handle.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


CAPTURE_ID_PATTERN = re.compile(r"^[0-9a-f]{64}$")
MAX_READ_IDS = 12
MAX_CROP_PIXELS = 2_000_000
MAX_SOURCE_IMAGE_PIXELS = 80_000_000
MAX_SOURCE_IMAGE_BYTES = 8_000_000


def _root() -> Path:
    configured = os.environ.get("LWA_EVIDENCE_DIR")
    return Path(configured).expanduser() if configured else Path.home() / ".cache/lwa-web/captures"


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temporary.write(data)
        name = temporary.name
    try:
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def save_capture(
    capture: dict[str, Any], raw_html: bytes, observations: list[dict[str, Any]],
    network_responses: list[dict[str, Any]] | None = None,
    images: list[dict[str, Any]] | None = None,
) -> str:
    """Persist inspected bytes and indexed evidence; return an opaque handle."""
    image_hashes = [hashlib.sha256(image["bytes"]).hexdigest() for image in images or []]
    identity = json.dumps({
        "requested": capture.get("requested"), "acquired_at_utc": capture.get("acquired_at_utc"),
        "content_sha256": capture.get("content_sha256"), "mode": capture.get("mode"),
        "image_sha256": image_hashes,
        "network_sha256": [response["sha256"] for response in network_responses or []],
    }, sort_keys=True).encode("utf-8")
    capture_id = hashlib.sha256(identity).hexdigest()
    folder = _root() / capture_id
    folder.mkdir(mode=0o700, parents=True, exist_ok=True)
    stored_images = []
    for image, image_hash in zip(images or [], image_hashes):
        image_bytes = image["bytes"]
        image_path = folder / "images" / image_hash
        _atomic_write(image_path, image_bytes)
        stored_images.append({key: value for key, value in image.items() if key != "bytes"} |
                             {"sha256": image_hash, "stored_path": str(image_path)})
    _atomic_write(folder / "page.html", raw_html)
    record = {"capture": capture | {"id": capture_id}, "observations": observations,
              "network_responses": network_responses or [], "images": stored_images}
    _atomic_write(folder / "evidence.json", json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"))
    return capture_id


def _load(capture_id: str) -> tuple[dict[str, Any], Path]:
    if not CAPTURE_ID_PATTERN.fullmatch(capture_id):
        raise ValueError("capture_id must be a 64-character lowercase hex handle")
    folder = _root() / capture_id
    path = folder / "evidence.json"
    if not path.is_file():
        raise FileNotFoundError("capture handle not found in this evidence store")
    return json.loads(path.read_text(encoding="utf-8")), folder


def inspect_evidence(capture_id: str, evidence_ids: list[str]) -> dict[str, Any]:
    """Resolve exact saved observations and bounded source excerpts."""
    if len(evidence_ids) > MAX_READ_IDS:
        raise ValueError(f"at most {MAX_READ_IDS} evidence IDs per call")
    record, folder = _load(capture_id)
    observations = {item["id"]: item for item in record["observations"]}
    html = (folder / "page.html").read_text(encoding="utf-8", errors="replace")
    lines = html.splitlines()
    resolved = []
    missing = []
    for evidence_id in evidence_ids:
        item = observations.get(evidence_id)
        if item is None:
            missing.append(evidence_id)
            continue
        detail = dict(item)
        match = re.fullmatch(r"html:(\d+):(\d+)", str(item.get("locator", "")))
        if match:
            line_number, column = map(int, match.groups())
            if 0 < line_number <= len(lines):
                source_line = lines[line_number - 1]
                detail["source_excerpt"] = source_line[max(0, column - 240):column + 440]
        resolved.append(detail)
    return {"capture": record["capture"], "observations": resolved,
            "missing_evidence_ids": missing, "saved_images": record["images"]}


def inspect_image_crop(
    capture_id: str, image_sha256: str, bbox: list[int] | None = None,
) -> tuple[dict[str, Any], bytes]:
    """Return bounded PNG pixels from an image belonging to this saved capture.

    An omitted bbox returns an orientation preview when the source is too large.
    Coordinates always refer to the original image, not to that preview.
    """
    if not CAPTURE_ID_PATTERN.fullmatch(image_sha256):
        raise ValueError("image_sha256 must be a 64-character lowercase hex digest")
    record, folder = _load(capture_id)
    image = next((item for item in record["images"] if item["sha256"] == image_sha256), None)
    if image is None:
        raise ValueError("image hash is not part of this capture")
    path = folder / "images" / image_sha256
    if path.stat().st_size > MAX_SOURCE_IMAGE_BYTES:
        raise ValueError("saved image exceeds byte limit")
    source_bytes = path.read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != image_sha256:
        raise ValueError("saved image bytes do not match the capture manifest")
    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("Pillow is required for image crop retrieval") from error
    with Image.open(io.BytesIO(source_bytes)) as source:
        width, height = source.size
        if width * height > MAX_SOURCE_IMAGE_PIXELS:
            raise ValueError("saved image dimensions exceed pixel limit")
        if bbox is None:
            if width * height <= MAX_CROP_PIXELS:
                region = source.copy()
                selected = [0, 0, width, height]
                preview = False
            else:
                region = source.copy()
                region.thumbnail((1400, 1400))
                selected = [0, 0, width, height]
                preview = True
        else:
            if (len(bbox) != 4 or any(type(value) is not int for value in bbox)):
                raise ValueError("bbox must be [left, top, right, bottom] in original pixels")
            left, top, right, bottom = bbox
            if not (0 <= left < right <= width and 0 <= top < bottom <= height):
                raise ValueError("bbox is outside the saved image")
            if (right - left) * (bottom - top) > MAX_CROP_PIXELS:
                raise ValueError("crop exceeds pixel limit")
            region = source.crop((left, top, right, bottom))
            selected = bbox
            preview = False
        output = io.BytesIO()
        region.save(output, format="PNG")
    metadata = {
        "capture_id": capture_id, "source_image_sha256": image_sha256,
        "source_path_or_url": image.get("source_path") or image.get("url"),
        "source_html_locator": image.get("html_locator"),
        "original_dimensions": [width, height], "bbox_original_pixels": selected,
        "preview_downscaled": preview, "returned_dimensions": list(region.size),
        "returned_png_sha256": hashlib.sha256(output.getvalue()).hexdigest(),
        "source_acquired_at_utc": image.get("acquired_at_utc"),
        "human_visibility": "unverified",
        "source_kind": "live_referenced_asset" if image.get("url") else "saved_snapshot_image",
    }
    return metadata, output.getvalue()


def check_claim(capture_id: str, claim: str, evidence_ids: list[str]) -> dict[str, Any]:
    """Confirm only literal source quotations; abstain on semantic inference.

    A matching quote supports a statement about what the captured source says.
    It does not verify stock, physical compatibility, current facts, or visual
    visibility. Contradiction needs a subject-bound semantic adjudicator and is
    deliberately not guessed from a substring or a purchase control.
    """
    inspected = inspect_evidence(capture_id, evidence_ids)
    normalize = lambda value: " ".join(value.casefold().split())
    literal_matches = [item["id"] for item in inspected["observations"]
                       if item.get("state") != "ocr_candidate" and
                       normalize(str(item.get("text", ""))) == normalize(claim)]
    status = "supported" if literal_matches else "insufficient_evidence"
    return {"capture_id": capture_id, "claim": claim, "status": status,
            "scope": "literal_text_in_captured_source" if literal_matches else "unresolved_semantic_claim",
            "supporting_evidence_ids": literal_matches,
            "missing_evidence_ids": inspected["missing_evidence_ids"],
            "reason": ("Exact observation text matched; this does not establish real-world truth or currentness."
                       if literal_matches else
                       "No exact observation quote matched. Semantic entailment or contradiction was not inferred.")}


def check_structured_claim(
    capture_id: str, subject: str, predicate: str, expected_value: str,
    evidence_ids: list[str], object_name: str = "",
) -> dict[str, Any]:
    """Check a narrow explicit assertion about one named subject in captured text.

    Only a single HTML text node containing the subject and a supported phrase
    can establish support or contradiction. Extractor summaries, OCR guesses,
    JSON fields, controls, and missing options cannot establish these claims.
    This describes a captured source statement, not actual stock/compatibility.
    """
    subject = " ".join(subject.split())
    object_name = " ".join(object_name.split())
    if not subject or len(subject) > 120 or len(object_name) > 120:
        raise ValueError("subject is required; subject and object_name must be at most 120 characters")
    if predicate == "stock_status":
        if expected_value not in {"in_stock", "out_of_stock"} or object_name:
            raise ValueError("stock_status requires in_stock/out_of_stock and no object_name")
    elif predicate == "compatibility":
        if expected_value not in {"compatible", "incompatible"} or not object_name:
            raise ValueError("compatibility requires compatible/incompatible and object_name")
    else:
        raise ValueError("supported predicates: stock_status, compatibility")

    inspected = inspect_evidence(capture_id, evidence_ids)
    bound_subject = rf"(?<!\w){re.escape(subject)}(?!\w)"
    if predicate == "stock_status":
        patterns = {
            "in_stock": rf"{bound_subject}(?:\s+(?:is|are)\s+|\s*:\s*)in stock(?!\w)",
            "out_of_stock": rf"{bound_subject}(?:\s+(?:is|are)\s+|\s*:\s*)out of stock(?!\w)",
        }
    else:
        bound_object = rf"(?<!\w){re.escape(object_name)}(?!\w)"
        patterns = {
            "compatible": rf"{bound_subject}\s+(?:is|are)\s+compatible with\s+{bound_object}",
            "incompatible": rf"{bound_subject}\s+(?:is|are)\s+(?:not compatible|incompatible) with\s+{bound_object}",
        }
    matches: dict[str, list[str]] = {key: [] for key in patterns}
    for item in inspected["observations"]:
        if item.get("source") != "html_text_node" or item.get("state") != "observed_text":
            continue
        statement = " ".join(str(item.get("text", "")).split())
        for value, pattern in patterns.items():
            if re.search(pattern, statement, flags=re.IGNORECASE):
                matches[value].append(item["id"])

    opposite = next(value for value in patterns if value != expected_value)
    if matches[expected_value] and matches[opposite]:
        status, reason = "insufficient_evidence", "Conflicting explicit statements in the cited captured text."
    elif matches[expected_value]:
        status, reason = "supported", "Explicit subject-bound statement in captured HTML text."
    elif matches[opposite]:
        status, reason = "contradicted", "Explicit opposite statement for the same subject in captured HTML text."
    else:
        status, reason = "insufficient_evidence", "No supported explicit subject-bound phrase in the cited HTML text."
    return {
        "capture_id": capture_id, "subject": subject, "predicate": predicate,
        "expected_value": expected_value, "object_name": object_name,
        "status": status, "scope": "cited_captured_html_statements_only",
        "supporting_evidence_ids": matches[expected_value],
        "opposing_evidence_ids": matches[opposite],
        "missing_evidence_ids": inspected["missing_evidence_ids"], "reason": reason,
    }
