"""Compile source locations once; query-time work reads a reusable evidence index."""

from __future__ import annotations

import io
import json
import re
from importlib.metadata import version

from . import VERSION
from .store import digest, encode

COMPILER_VERSION = VERSION + ":compiler-2"
MAX_RECORDS = 12000
MAX_REGIONS = 128
CARD = re.compile(
    r"(?:^|[\s_-])(card|coupon|tile|product|testimonial|banner|promotion|panel|offer)(?:$|[\s_-])",
    re.IGNORECASE,
)
BLOCKS = {
    "p",
    "div",
    "section",
    "article",
    "li",
    "tr",
    "fieldset",
    "dt",
    "dd",
    "h1",
    "h2",
    "h3",
    "h4",
}
CHALLENGES = (
    "cf-mitigated",
    "checking your browser",
    "verify you are human",
    "attention required! | cloudflare",
    "cloudflare ray id",
)
STOP = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "by",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "page",
    "show",
    "the",
    "there",
    "this",
    "to",
    "what",
    "which",
    "with",
    "please",
    "tell",
    "me",
}


def norm(value):
    return " ".join(str(value).split())


def terms(value):
    # Include combining marks so Bengali words are not split into unrelated fragments.
    return {
        x
        for x in re.findall(r"[\w\u0980-\u09ff]+", str(value).casefold())
        if x not in STOP
    }


def locator(tag, numbers):
    if tag.get("data-lwa-node"):
        return "node:" + tag["data-lwa-node"]
    if tag.sourceline is not None:
        return f"html:{tag.sourceline}:{tag.sourcepos}"
    return "node:" + str(numbers.get(id(tag), 0))


def compile_capture(store, capture_id):
    key = "index:" + digest(
        encode([capture_id, COMPILER_VERSION, version("beautifulsoup4")])
    )
    hit = store.cached(key)
    if hit:
        return store.get(hit, "index"), True
    manifest = store.get(capture_id, "capture")
    raw = store.read_blob(manifest["html_sha256"])
    html = raw.decode("utf-8", errors="replace")
    blocked = any(marker in html[:100000].casefold() for marker in CHALLENGES)
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html, "html.parser")
    requires_render = bool(
        soup.find("style")
        or soup.find("link", rel="stylesheet")
        or any(
            n.get("src")
            or n.get("type", "").lower()
            not in {"application/ld+json", "application/json"}
            for n in soup.find_all("script")
        )
    )
    embedded = []
    for node in soup.find_all("script"):
        content = node.string or node.get_text()
        if node.get("type") in {"application/ld+json", "application/json"}:
            try:
                embedded.append(("script:" + str(len(embedded)), json.loads(content)))
            except (ValueError, RecursionError):
                pass
        for match in re.finditer(
            r"(?:window\.)?(?:__serviceState|__NEXT_DATA__)\s*=\s*", content
        ):
            try:
                data, _ = json.JSONDecoder().raw_decode(content[match.end() :])
                embedded.append(("script:" + str(len(embedded)), data))
            except (ValueError, RecursionError):
                pass
    for node in list(soup.find_all(True)):
        if node.attrs is None:
            continue
        style = (node.get("style") or "").replace(" ", "").lower()
        if (
            node.name in {"script", "style", "noscript", "head", "svg", "iframe"}
            or node.has_attr("hidden")
            or node.get("aria-hidden") == "true"
            or node.get("data-lwa-visible") == "false"
            or "display:none" in style
            or "visibility:hidden" in style
        ):
            node.decompose()
    nodes = list(soup.find_all(True))
    numbers = {id(node): i + 1 for i, node in enumerate(nodes)}
    geometry = {entry["locator"]: entry for entry in manifest["geometry"]}
    texts = {
        id(node): norm(node.get_text(" ", strip=True))
        for node in nodes
        if node.name in BLOCKS
    }
    is_card = lambda node: (
        node.name in {"article", "li", "tr", "fieldset"}
        or bool(CARD.search(" ".join(node.get("class", []))))
    )
    groups, group_parts = {}, {}
    for text in soup.find_all(string=True):
        if not isinstance(text, NavigableString) or not norm(text):
            continue
        ancestors = [
            p for p in text.parents if p.name not in {"[document]", "body", "html"}
        ]
        nearest = next((p for p in ancestors if p.name in BLOCKS), text.parent)
        card = next((p for p in ancestors if is_card(p)), None)
        # Never join neighboring cards through their shared section.
        section = next(
            (
                p
                for p in ancestors
                if p.name == "section"
                and len(texts.get(id(p), "")) <= 1600
                and not p.find(is_card)
            ),
            None,
        )
        group = card or section or nearest
        if len(texts.get(id(group), "")) > 1600:
            group = nearest
        groups[id(group)] = group
        group_parts.setdefault(id(group), []).append(norm(text))
    evidence = []
    coverage = ["interactive_states_unchecked", "external_css_visibility_unverified"]
    if soup.find("img"):
        coverage.append("image_asset_coverage_unverified")
    if geometry:
        coverage.remove("external_css_visibility_unverified")

    def list_context(node):
        heading = node.find_previous_sibling(["h1", "h2", "h3", "h4"])
        if heading is None and node.parent:
            heading = node.parent.find(["h1", "h2", "h3", "h4"], recursive=False)
        return norm(
            node.get("aria-label")
            or (heading.get_text(" ", strip=True) if heading else "")
        )

    def heading_context(node):
        if is_card(node):
            return ""
        for parent in node.parents:
            if parent.name in {"html", "body", "[document]"}:
                break
            headings = parent.find_all(["h1", "h2", "h3", "h4"], recursive=False)
            if len(headings) == 1:
                return norm(headings[0].get_text(" ", strip=True))
            if len(headings) > 1:
                break
        return ""

    for group in sorted(groups.values(), key=lambda g: numbers.get(id(g), 0)):
        if len(evidence) >= MAX_RECORDS:
            coverage.append("text_index_truncated")
            break
        text = norm(" ".join(group_parts[id(group)]))
        if not text:
            continue
        loc = locator(group, numbers)
        sequence = None
        if group.name == "li" and group.parent.name in {"ul", "ol"}:
            siblings = group.parent.find_all("li", recursive=False)
            sequence = {
                "id": locator(group.parent, numbers),
                "position": next(i + 1 for i, s in enumerate(siblings) if s is group),
                "length": len(siblings),
            }
        fields = []
        for dt in group.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                fields.append(
                    [
                        norm(dt.get_text(" ", strip=True)),
                        norm(dd.get_text(" ", strip=True)),
                    ]
                )
        if group.name == "tr":
            cells = group.find_all(["th", "td"], recursive=False)
            if len(cells) == 2:
                fields.append(
                    [
                        norm(cells[0].get_text(" ", strip=True)),
                        norm(cells[1].get_text(" ", strip=True)),
                    ]
                )
        for node in group.find_all(["p", "span", "div"], recursive=False):
            if is_card(node):
                continue
            value = norm(node.get_text(" ", strip=True))
            if ":" in value and len(value) < 300:
                left, right = value.split(":", 1)
                if len(left) < 60:
                    fields.append([left, right.strip()])
        fields = [
            [label, value] for label, value in fields if label in text and value in text
        ]
        evidence.append(
            {
                "capture_id": capture_id,
                "source_kind": "dom_text",
                "source_sha256": manifest["html_sha256"],
                "locator": loc,
                "text": text[:1600],
                "truncated": len(text) > 1600,
                "tag": group.name,
                "human_visibility": "rendered" if loc in geometry else "unverified",
                "binding": "container",
                "fields": fields,
                "sequence": sequence,
                "context": list_context(group.parent)
                if sequence
                else heading_context(group),
                "geometry": geometry.get(loc),
                "order": numbers.get(id(group), 0),
            }
        )
    for node in soup.find_all(["ol", "ul"]):
        if len(evidence) >= MAX_RECORDS:
            coverage.append("text_index_truncated")
            break
        children = node.find_all("li", recursive=False)
        items = [norm(child.get_text(" ", strip=True)) for child in children]
        if not items or any(not item for item in items):
            continue
        text = " ".join(items)
        loc = locator(node, numbers)
        evidence.append(
            {
                "capture_id": capture_id,
                "source_kind": "dom_sequence",
                "source_sha256": manifest["html_sha256"],
                "locator": loc,
                "text": text[:1600],
                "items": items[:12],
                "context": list_context(node),
                "tag": node.name,
                "truncated": len(text) > 1600
                or len(items) > 12
                or any(child.find(["ul", "ol"]) for child in children),
                "human_visibility": "rendered" if loc in geometry else "unverified",
                "binding": "ordered_container",
                "geometry": geometry.get(loc),
                "order": numbers.get(id(node), 0),
            }
        )

    # Scalar JSON fields retain an object context and a JSON path; never call them visible.
    def walk(value, path, origin, sha, parent=None, depth=0):
        if len(evidence) >= MAX_RECORDS or depth > 12:
            if "data_index_truncated" not in coverage:
                coverage.append("data_index_truncated")
            return
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, path + "." + str(k), origin, sha, value, depth + 1)
        elif isinstance(value, list):
            for i, v in enumerate(value[:500]):
                walk(v, path + f"[{i}]", origin, sha, None, depth + 1)
            if len(value) > 500:
                coverage.append("data_array_truncated")
        elif value is not None:
            context = {
                k: v
                for k, v in (parent or {}).items()
                if isinstance(v, (str, int, float, bool))
            }
            context_text = norm(json.dumps(context, ensure_ascii=False))
            evidence.append(
                {
                    "capture_id": capture_id,
                    "source_kind": origin,
                    "source_sha256": sha,
                    "locator": path,
                    "text": str(value)[:1600],
                    "context": context_text[:1600],
                    "field": path.rsplit(".", 1)[-1],
                    "truncated": len(str(value)) > 1600 or len(context_text) > 1600,
                    "human_visibility": "unverified",
                    "binding": "json_object",
                    "order": len(evidence),
                }
            )

    for origin, value in embedded:
        walk(value, origin + ":$", "embedded_json", manifest["html_sha256"])
    for i, response in enumerate(manifest["network"]):
        walk(
            json.loads(store.read_blob(response["sha256"])),
            f"response:{i}:$",
            "network_json",
            response["sha256"],
        )
    regions = []
    for image in manifest["images"]:
        width, height = image["width"], image["height"]
        # A region is identified by source bytes and coordinates, never by a filename.
        boxes = []
        if image["role"] == "rendered_screenshot":
            for g in manifest["geometry"]:
                x1, y1, x2, y2 = map(int, g["bbox"])
                if (
                    g.get("tag") == "img"
                    and 0 <= x1 < x2 <= width
                    and 0 <= y1 < y2 <= height
                    and (x2 - x1) * (y2 - y1) <= 2_000_000
                ):
                    boxes.append(
                        (
                            [x1, y1, x2, y2],
                            g.get("alt", "")[:300],
                            g["locator"],
                            "dom_image_geometry",
                        )
                    )
            for item in evidence:
                g = item.get("geometry")
                if g:
                    x1, y1, x2, y2 = map(int, g["bbox"])
                    if (
                        0 <= x1 < x2 <= width
                        and 0 <= y1 < y2 <= height
                        and (x2 - x1) * (y2 - y1) <= 2_000_000
                    ):
                        boxes.append(
                            (
                                [x1, y1, x2, y2],
                                item["text"][:300],
                                item["locator"],
                                "dom_geometry",
                            )
                        )
        if image.get("locator"):
            anchor = next(
                (e["text"] for e in evidence if e["locator"] == image["locator"]), ""
            )
        else:
            anchor = ""
        if width * height <= 1_000_000:
            boxes.append(
                ([0, 0, width, height], anchor[:300], image.get("locator"), "image")
            )
        else:
            for y in range(0, height, 640):
                for x in range(0, width, 640):
                    boxes.append(
                        (
                            [x, y, min(x + 768, width), min(y + 768, height)],
                            anchor[:300],
                            None,
                            "tile",
                        )
                    )
                    if len(boxes) >= MAX_REGIONS:
                        break
                if len(boxes) >= MAX_REGIONS:
                    break
        seen = set()
        for box, anchor, loc, binding in boxes:
            if len(regions) >= MAX_REGIONS:
                coverage.append("visual_region_index_truncated")
                break
            if tuple(box) in seen:
                continue
            seen.add(tuple(box))
            regions.append(
                {
                    "capture_id": capture_id,
                    "source_kind": "image_region",
                    "source_sha256": image["sha256"],
                    "bbox": box,
                    "text": "",
                    "anchor": anchor,
                    "locator": loc,
                    "binding": binding,
                    "order": len(regions),
                    "human_visibility": "saved_pixels",
                }
            )
    if manifest["images"]:
        coverage.append("image_text_unverified")
    evidence_ids = store.put_many("ev", evidence + regions)
    records = [
        dict(item, id=handle) for item, handle in zip(evidence + regions, evidence_ids)
    ]
    result = {
        "capture_id": capture_id,
        "version": COMPILER_VERSION,
        "blocked": blocked,
        "requires_render": requires_render,
        "records": records,
        "coverage": sorted(set(coverage)),
        "html_bytes": len(raw),
        "image_bytes": sum(
            len(store.read_blob(i["sha256"])) for i in manifest["images"]
        ),
    }
    return store.get(store.cache(key, store.put("index", result)), "index"), False


def crop_pixels(store, record, max_pixels=1_000_000):
    from PIL import Image

    with Image.open(io.BytesIO(store.read_blob(record["source_sha256"]))) as opened:
        box = record["bbox"]
        width, height = opened.size
        if len(box) != 4 or not (
            0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height
        ):
            raise ValueError("invalid source crop")
        crop = opened.crop(box).convert("RGB")
        if crop.width * crop.height > max_pixels:
            scale = (max_pixels / (crop.width * crop.height)) ** 0.5
            crop = crop.resize(
                (max(1, int(crop.width * scale)), max(1, int(crop.height * scale)))
            )
        output = io.BytesIO()
        crop.save(output, format="PNG")
        return output.getvalue(), list(crop.size)
