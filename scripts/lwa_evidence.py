"""Evidence-preserving core for the LWA-Web MCP tool.

This module deliberately separates saved snapshots from live HTTP responses. It
does not claim that raw HTML is a hydrated, human-visible page. Browser capture
is bounded; live image acquisition is also bounded and requires local OCR tools.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

try:
    from .lwa_evidence_store import save_capture
except ImportError:  # Direct execution through the MCP wrapper.
    from lwa_evidence_store import save_capture


MAX_HTML_BYTES = 4_000_000
MAX_EVIDENCE = 12
MAX_IMAGES = 3
MAX_IMAGE_BYTES = 2_000_000
MAX_SNAPSHOT_IMAGE_BYTES = 8_000_000
MAX_NETWORK_RESPONSES = 8
MAX_NETWORK_RESPONSE_BYTES = 500_000
STOPWORDS = {
    "a", "an", "and", "are", "at", "by", "does", "for", "from", "how", "in",
    "is", "it", "of", "on", "or", "page", "show", "the", "there", "this",
    "to", "what", "which", "with",
}
CHALLENGE_MARKERS = (
    "cf-mitigated", "checking your browser", "verify you are human",
    "attention required! | cloudflare", "challenges.cloudflare.com",
    "cloudflare ray id",
)


def _tokens(value: str) -> set[str]:
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    return {word for word in re.findall(r"\w+", value.casefold())
            if len(word) > 1 and word not in STOPWORDS}


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class PageTextParser(HTMLParser):
    """Collect raw-HTML text with line pointers and candidate image references."""

    SKIP = {"script", "style", "svg", "noscript", "head", "iframe"}
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_stack: list[str] = []
        self.text_nodes: list[dict[str, Any]] = []
        self.images: list[dict[str, str]] = []
        self.buttons: list[dict[str, Any]] = []
        self._button: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        hidden = (tag in self.SKIP or "hidden" in attributes or
                  attributes.get("aria-hidden") == "true" or
                  "display:none" in (attributes.get("style") or "").replace(" ", "").lower())
        if self.skip_stack:
            if tag not in self.VOID:
                self.skip_stack.append(tag)
            return
        if hidden:
            if tag not in self.VOID:
                self.skip_stack.append(tag)
            return
        style = attributes.get("style") or ""
        if "background" in style.lower():
            for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", style, re.IGNORECASE):
                self.images.append({"src": match.group(1), "alt": "", "title": "",
                                    "kind": "css_background", "locator": f"html:{self.getpos()[0]}:{self.getpos()[1]}"})
        if tag == "img":
            source = attributes.get("src") or attributes.get("data-src") or ""
            if source.startswith("data:") and attributes.get("srcset"):
                source = attributes["srcset"].split(",")[0].strip().split()[0]
            self.images.append({
                "src": source,
                "alt": attributes.get("alt") or "",
                "title": attributes.get("title") or "",
                "kind": "img",
                "locator": f"html:{self.getpos()[0]}:{self.getpos()[1]}",
            })
        elif tag == "button":
            self._button = {
                "label_parts": [],
                "disabled": "disabled" in attributes,
                "locator": f"html:{self.getpos()[0]}:{self.getpos()[1]}",
            }

    def handle_endtag(self, tag: str) -> None:
        if self.skip_stack:
            if tag in self.skip_stack:
                while self.skip_stack:
                    if self.skip_stack.pop() == tag:
                        break
            return
        if tag == "button" and self._button is not None:
            self._button["label"] = " ".join(self._button.pop("label_parts")).strip()
            self.buttons.append(self._button)
            self._button = None

    def handle_data(self, data: str) -> None:
        if self.skip_stack:
            return
        value = " ".join(data.split())
        if value:
            self.text_nodes.append({"text": value, "locator": f"html:{self.getpos()[0]}:{self.getpos()[1]}"})
            if self._button is not None:
                self._button["label_parts"].append(value)


def _extractor_views(html: str, node_text: str) -> tuple[dict[str, str], dict[str, str]]:
    """Run available text extractors; report missing dependencies explicitly."""
    views = {"html_text_nodes": node_text}
    unavailable = {}
    try:
        import trafilatura
        views["trafilatura"] = trafilatura.extract(html, favor_recall=True) or ""
    except Exception as error:
        unavailable["trafilatura"] = type(error).__name__
    try:
        from readability import Document
        from bs4 import BeautifulSoup
        views["readability"] = BeautifulSoup(Document(html).summary(), "html.parser").get_text(" ", strip=True)
    except Exception as error:
        unavailable["readability"] = type(error).__name__
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "svg", "noscript"]):
            tag.decompose()
        views["beautifulsoup"] = soup.get_text(" ", strip=True)
    except Exception as error:
        unavailable["beautifulsoup"] = type(error).__name__
    try:
        import html2text
        converter = html2text.HTML2Text()
        converter.body_width = 0
        views["html2text"] = converter.handle(html)
    except Exception as error:
        unavailable["html2text"] = type(error).__name__
    return views, unavailable


def _embedded_json_matches(html: str, terms: set[str], limit: int = 4) -> list[dict[str, str]]:
    """Find relevant fields in JSON-LD and known embedded page state, without claiming visibility."""
    if not terms:
        return []
    candidates: list[tuple[str, Any]] = []
    for match in re.finditer(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                             html, re.IGNORECASE | re.DOTALL):
        try:
            candidates.append(("json_ld", json.loads(match.group(1))))
        except json.JSONDecodeError:
            continue
    for name in ("window.__serviceState", "window.__NEXT_DATA__"):
        match = re.search(re.escape(name) + r"\s*=\s*", html)
        if match:
            try:
                value, _ = json.JSONDecoder().raw_decode(html[match.end():])
                candidates.append((name, value))
            except json.JSONDecodeError:
                pass
    found: list[tuple[int, dict[str, str]]] = []
    visited = 0

    def walk(value: Any, path: str, source: str, depth: int = 0) -> None:
        nonlocal visited
        visited += 1
        if visited > 100_000 or depth > 12:
            return
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{path}.{key}", source, depth + 1)
                if visited > 100_000:
                    return
        elif isinstance(value, list):
            for index, child in enumerate(value[:100]):
                walk(child, f"{path}[{index}]", source, depth + 1)
                if visited > 100_000:
                    return
        elif value is not None:
            path_hits = _tokens(path) & terms
            value_hits = _tokens(str(value)) & terms
            if path_hits or value_hits:
                score = len(path_hits) * 2 + len(value_hits)
                found.append((score, {"source": source, "locator": path, "text": str(value)[:300]}))

    for name, data in candidates:
        walk(data, "$", name)
    found.sort(key=lambda result: -result[0])
    return [entry for _, entry in found[:limit]]


def _network_json_matches(responses: list[dict[str, Any]], terms: set[str], limit: int = 4) -> list[dict[str, str]]:
    """Search passively captured page JSON without labeling it visible UI."""
    if not terms:
        return []
    found: list[tuple[int, dict[str, str]]] = []
    visited = 0

    def walk(value: Any, path: str, response: dict[str, Any], depth: int = 0) -> None:
        nonlocal visited
        visited += 1
        if visited > 50_000 or depth > 12:
            return
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{path}.{key}", response, depth + 1)
                if visited > 50_000:
                    return
        elif isinstance(value, list):
            for index, child in enumerate(value[:100]):
                walk(child, f"{path}[{index}]", response, depth + 1)
                if visited > 50_000:
                    return
        elif value is not None:
            path_hits = _tokens(path) & terms
            value_hits = _tokens(str(value)) & terms
            if path_hits or value_hits:
                found.append((2 * len(path_hits) + len(value_hits), {
                    "source": "network_json", "locator": path, "text": str(value)[:300],
                    "response_url": response["url"], "response_sha256": response["sha256"],
                    "response_captured_at_utc": response["captured_at_utc"],
                }))

    for response in responses:
        walk(response["json"], "$", response)
    found.sort(key=lambda item: -item[0])
    return [item for _, item in found[:limit]]


def _ocr_file(path: Path, terms: set[str]) -> tuple[list[dict[str, Any]], str | None]:
    if not path.is_file():
        return [], "image file missing"
    if not shutil.which("tesseract"):
        return [], "Tesseract OCR unavailable"
    try:
        result = subprocess.run(
            ["tesseract", str(path), "stdout", "-l", "eng+ben", "--psm", "11", "tsv"],
            capture_output=True, text=True, timeout=20, check=False,
        )
    except subprocess.TimeoutExpired:
        return [], "OCR timed out"
    if result.returncode:
        return [], (result.stderr.strip() or "OCR failed")[:250]
    rows = result.stdout.splitlines()
    if not rows:
        return [], "OCR produced no text"
    header = rows[0].split("\t")
    lines: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    for row in rows[1:]:
        parts = row.split("\t")
        if len(parts) != len(header):
            continue
        item = dict(zip(header, parts))
        try:
            confidence = float(item.get("conf", "-1"))
        except ValueError:
            continue
        if confidence >= 50 and item.get("text", "").strip():
            key = tuple(item.get(name, "") for name in ("page_num", "block_num", "par_num", "line_num"))
            lines.setdefault(key, []).append(item)
    grouped = []
    for words in lines.values():
        text = " ".join(word["text"] for word in words)
        left = min(int(word["left"]) for word in words)
        top = min(int(word["top"]) for word in words)
        right = max(int(word["left"]) + int(word["width"]) for word in words)
        bottom = max(int(word["top"]) + int(word["height"]) for word in words)
        grouped.append({"text": text, "bbox": [left, top, right, bottom],
                        "confidence_min": min(float(word["conf"]) for word in words)})
    if not grouped:
        return [], "OCR produced no confident text"
    selected = [line for line in grouped if not terms or _tokens(line["text"]) & terms]
    if terms and not selected:
        return [], "OCR found text, but no question-term match in the inspected image"
    if not terms:
        selected = grouped[:10]
    image_hash = _sha(path.read_bytes())
    evidence = [{
        "source": "ocr_tesseract", "locator": str(path),
        "text": line["text"][:500],
        "image_sha256": image_hash,
        "confidence_min": line["confidence_min"], "bbox": line["bbox"],
    } for line in selected[:10]]
    return evidence, None if evidence else "OCR produced no confident text"


def _acquire_live_images(images: list[dict[str, str]], base_url: str, terms: set[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    """Fetch a few referenced raster images and OCR their actual bytes."""
    if not shutil.which("tesseract"):
        return [], [], [{"reason": "Tesseract OCR unavailable; no image pixels fetched"}]
    ranked = []
    seen_urls = set()
    for index, image in enumerate(images):
        source = image.get("src", "")
        if not source:
            continue
        url = urljoin(base_url, source)
        if urlparse(url).scheme not in {"http", "https"} or url in seen_urls:
            continue
        seen_urls.add(url)
        description = " ".join([source, image.get("alt", ""), image.get("title", "")])
        score = 10 * len(_tokens(description) & terms)
        if re.search(r"banner|hero|campaign|offer|promo|puja", description, re.IGNORECASE):
            score += 2
        ranked.append((-score, index, image, url))
    ranked.sort()
    observations: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for _, _, image, url in ranked[:MAX_IMAGES]:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "LWA-Web/0.1 (research extraction)"})
            with urllib.request.urlopen(request, timeout=8) as response:
                content_type = response.headers.get_content_type()
                if content_type not in {"image/png", "image/jpeg", "image/webp", "image/gif", "image/bmp"}:
                    raise ValueError(f"unsupported image content type: {content_type}")
                image_bytes = response.read(MAX_IMAGE_BYTES + 1)
                if len(image_bytes) > MAX_IMAGE_BYTES:
                    raise ValueError("image exceeds byte limit")
                final_url = response.geturl()
            suffix = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
                      "image/gif": ".gif", "image/bmp": ".bmp"}[content_type]
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temporary:
                temporary.write(image_bytes)
                temporary_path = Path(temporary.name)
            try:
                ocr_items, error = _ocr_file(temporary_path, terms)
            finally:
                temporary_path.unlink(missing_ok=True)
            image_hash = _sha(image_bytes)
            artifacts.append({"bytes": image_bytes, "url": final_url,
                              "html_locator": image["locator"], "content_type": content_type,
                              "acquired_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")})
            if error:
                errors.append({"url": final_url, "reason": error})
            for item in ocr_items:
                item.update({"locator": image["locator"], "image_url": final_url,
                             "image_sha256": image_hash, "human_visibility": "unverified"})
                observations.append(item)
        except Exception as error:
            errors.append({"url": url, "reason": str(error)[:180]})
    return observations, artifacts, errors


def _fetch_live(url: str) -> tuple[bytes, str, int | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "LWA-Web/0.1 (research extraction)"})
    try:
        response = urllib.request.urlopen(request, timeout=12)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        raw = response.read(MAX_HTML_BYTES + 1)
        if len(raw) > MAX_HTML_BYTES:
            raise ValueError(f"HTML response exceeds {MAX_HTML_BYTES} bytes")
        return raw, response.geturl(), response.status


def _fetch_browser(url: str) -> tuple[bytes, str, int | None, list[dict[str, Any]]]:
    """Capture a bounded rendered DOM; stable body text is not proof of full hydration."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError("Playwright is unavailable for browser rendering") from error
    with sync_playwright() as playwright:
        executable = os.environ.get("CHROMIUM_EXECUTABLE") or shutil.which("chromium")
        browser = playwright.chromium.launch(headless=True, executable_path=executable)
        try:
            page = browser.new_page()
            json_responses = []
            page.on("response", lambda response: json_responses.append(response)
                    if "json" in response.headers.get("content-type", "").lower() else None)
            response = page.goto(url, wait_until="domcontentloaded", timeout=12_000)
            previous = None
            for _ in range(6):
                page.wait_for_timeout(400)
                current = page.locator("body").inner_text(timeout=2_000)
                if current and current == previous:
                    break
                previous = current
            raw = page.content().encode("utf-8")
            if len(raw) > MAX_HTML_BYTES:
                raise ValueError(f"Rendered HTML exceeds {MAX_HTML_BYTES} bytes")
            captured_json = []
            for candidate in json_responses[:MAX_NETWORK_RESPONSES]:
                try:
                    body = candidate.body()
                    if len(body) > MAX_NETWORK_RESPONSE_BYTES:
                        continue
                    captured_json.append({
                        "url": candidate.url, "status": candidate.status, "sha256": _sha(body),
                        "bytes": len(body),
                        "captured_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                        "json": json.loads(body),
                    })
                except (ValueError, RuntimeError, OSError):
                    continue
            return raw, page.url, response.status if response else None, captured_json
        finally:
            browser.close()


def inspect_page(
    target: str,
    question: str = "",
    mode: str = "live",
    snapshot_captured_at_utc: str | None = None,
    image_paths: list[str] | None = None,
    render: str = "http",
) -> dict[str, Any]:
    """Inspect a live HTTP URL or an explicit saved HTML snapshot.

    This returns evidence, not a generated answer. Live mode has no implicit
    benchmark cache. Snapshot mode never fetches the network, including images.
    """
    if mode not in {"live", "snapshot"}:
        raise ValueError("mode must be 'live' or 'snapshot'")
    if render not in {"http", "browser"}:
        raise ValueError("render must be 'http' or 'browser'")
    if mode == "snapshot" and render != "http":
        raise ValueError("browser rendering is only valid in live mode")
    parsed = urlparse(target)
    if mode == "live" and parsed.scheme not in {"http", "https"}:
        raise ValueError("live mode requires an HTTP(S) URL")
    if mode == "snapshot" and parsed.scheme:
        raise ValueError("snapshot mode requires a local HTML path")
    if snapshot_captured_at_utc and mode != "snapshot":
        raise ValueError("snapshot timestamp is only valid in snapshot mode")
    if image_paths and mode != "snapshot":
        raise ValueError("local image_paths are only valid with snapshot mode")

    started = time.perf_counter()
    requested_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    network_responses: list[dict[str, Any]] = []
    try:
        if mode == "snapshot":
            path = Path(target)
            raw = path.read_bytes()
            if len(raw) > MAX_HTML_BYTES:
                raise ValueError(f"HTML snapshot exceeds {MAX_HTML_BYTES} bytes")
            final_url, http_status = None, None
        else:
            if render == "browser":
                raw, final_url, http_status, network_responses = _fetch_browser(target)
            else:
                raw, final_url, http_status = _fetch_live(target)
    except Exception as error:
        return {
            "capture": {"requested": target, "mode": mode, "access": "failed",
                        "requested_at_utc": requested_at, "error": str(error)[:300]},
            "observations": [], "unresolved": [{"question": question, "state": "access_failed"}],
            "resource_usage": {"elapsed_ms": round((time.perf_counter() - started) * 1000, 2)},
        }

    acquired_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    html = raw.decode("utf-8", errors="replace")
    lowered = html[:100_000].casefold()
    blocked = http_status in {401, 403, 429} or any(marker in lowered for marker in CHALLENGE_MARKERS)
    http_failed = http_status is not None and http_status >= 400 and not blocked
    capture = {
        "requested": target, "final_url": final_url, "mode": mode,
        "acquisition": "saved_snapshot" if mode == "snapshot" else f"live_{render}",
        "access": "blocked" if blocked else "failed" if http_failed else "ok",
        "http_status": http_status,
        "requested_at_utc": requested_at, "acquired_at_utc": acquired_at,
        "captured_at_utc": snapshot_captured_at_utc if mode == "snapshot" else acquired_at,
        "captured_at_source": ("caller_supplied" if snapshot_captured_at_utc else "unknown")
                              if mode == "snapshot" else "tool_clock",
        "content_sha256": _sha(raw), "input_bytes": len(raw),
        "render_state": ("saved_unknown" if mode == "snapshot" else
                         "browser_dom_unverified" if render == "browser" else "initial_html"),
    }
    if blocked or http_failed:
        capture["id"] = save_capture(capture, raw, [], network_responses)
        return {"capture": capture, "observations": [],
                "unresolved": [{"question": question,
                                "state": "access_blocked" if blocked else "http_error"}],
                "resource_usage": {"elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                                   "input_bytes": len(raw)}}

    parser = PageTextParser()
    parser.feed(html)
    terms = _tokens(question)
    node_text = "\n".join(node["text"] for node in parser.text_nodes)
    views, unavailable = _extractor_views(html, node_text)
    candidates: list[dict[str, Any]] = []
    for node in parser.text_nodes:
        candidates.append({"source": "html_text_node", **node, "human_visibility": "unverified"})
    for name, output in views.items():
        if name == "html_text_nodes":
            continue
        for match in re.finditer(r"[^\n.!?]{1,280}(?:[.!?]|$)", output):
            value = " ".join(match.group().split())
            if value:
                candidates.append({"source": f"extractor:{name}", "locator": f"offset:{match.start()}",
                                   "text": value, "human_visibility": "unverified"})
    for entry in _embedded_json_matches(html, terms):
        candidates.append({**entry, "human_visibility": "unverified"})
    for entry in _network_json_matches(network_responses, terms):
        candidates.append({**entry, "human_visibility": "unverified"})

    ranked = []
    for candidate in candidates:
        searchable = _tokens(candidate["text"])
        if candidate["source"] in {"json_ld", "window.__serviceState", "window.__NEXT_DATA__", "network_json"}:
            searchable |= _tokens(candidate["locator"])
        overlap = len(terms & searchable)
        if terms and not overlap:
            continue
        score = overlap * 10 + (1 if candidate["source"] == "html_text_node" else 0)
        ranked.append((score, candidate))
    ranked.sort(key=lambda entry: -entry[0])
    observations = []
    seen: dict[tuple[str, str], dict[str, Any]] = {}
    text_limit = MAX_EVIDENCE - 4 if (parser.images or image_paths) else MAX_EVIDENCE
    for _, candidate in ranked:
        normalized = " ".join(candidate["text"].casefold().split())
        key = (normalized, candidate["source"])
        if key in seen:
            if len(seen[key]["also_seen_at"]) < 4:
                seen[key]["also_seen_at"].append(candidate["locator"])
            continue
        observation = {"id": f"obs-{len(observations)+1:03}", "state": "observed_text",
                       "capture_sha256": capture["content_sha256"], "also_seen_at": [], **candidate}
        seen[key] = observation
        observations.append(observation)
        if len(observations) >= text_limit:
            break

    ocr_errors = []
    image_artifacts: list[dict[str, Any]] = []
    if image_paths:
        for image_path in image_paths[:3]:
            path = Path(image_path)
            if not path.is_file() or path.stat().st_size > MAX_SNAPSHOT_IMAGE_BYTES:
                ocr_errors.append({"path": image_path, "error": "image missing or exceeds byte limit"})
                continue
            image_bytes = path.read_bytes()
            ocr_observations, error = _ocr_file(path, terms)
            image_artifacts.append({"bytes": image_bytes, "source_path": str(path),
                                    "acquired_at_utc": acquired_at})
            if error:
                ocr_errors.append({"path": image_path, "error": error})
            for item in ocr_observations:
                if len(observations) >= MAX_EVIDENCE:
                    break
                item.update({"id": f"obs-{len(observations)+1:03}", "state": "ocr_candidate",
                             "exactness": "unverified",
                             "human_visibility": "unverified", "locator": str(path)})
                observations.append(item)
    elif mode == "live" and parser.images:
        live_ocr, image_artifacts, live_errors = _acquire_live_images(parser.images, final_url or target, terms)
        ocr_errors.extend(live_errors)
        for item in live_ocr:
            if len(observations) >= MAX_EVIDENCE:
                break
            item.update({"id": f"obs-{len(observations)+1:03}", "state": "ocr_candidate",
                         "exactness": "unverified"})
            observations.append(item)

    # Use any visual reservation that OCR did not consume for the remaining text.
    for _, candidate in ranked:
        if len(observations) >= MAX_EVIDENCE:
            break
        normalized = " ".join(candidate["text"].casefold().split())
        key = (normalized, candidate["source"])
        if key in seen:
            continue
        observation = {"id": f"obs-{len(observations)+1:03}", "state": "observed_text",
                       "capture_sha256": capture["content_sha256"], "also_seen_at": [], **candidate}
        seen[key] = observation
        observations.append(observation)

    unresolved = []
    if terms & {"stock", "inventory", "compatible", "incompatible", "fits"}:
        unresolved.append({"question": question, "state": "unknown",
                           "reason": "This component has not verified an explicit statement bound to the requested product and variant; controls or missing options alone are insufficient."})
    elif terms and not observations:
        unresolved.append({"question": question, "state": "not_observed_in_inspected_sources"})
    if parser.images and (mode == "snapshot" and not image_paths or
                          mode == "live" and len(image_artifacts) < len(parser.images)):
        unresolved.append({"state": "image_unchecked", "count": len(parser.images),
                           "inspected_assets": len(image_artifacts),
                           "reason": "Some referenced image pixels were not inspected; alt text and filenames are not OCR."})
    if ocr_errors:
        no_match = [entry for entry in ocr_errors if "no question-term match" in str(entry.get("error") or entry.get("reason"))]
        other_errors = [entry for entry in ocr_errors if entry not in no_match]
        if no_match:
            unresolved.append({"state": "ocr_no_question_match", "details": no_match,
                               "reason": "The inspected image yielded no matching OCR line; this does not prove the fact is absent from other images or states."})
        if other_errors:
            unresolved.append({"state": "ocr_unavailable_or_failed", "details": other_errors})
    if mode == "snapshot":
        unresolved.append({"state": "historical_snapshot",
                           "reason": "Saved capture is not proof of current website state."})
    else:
        unresolved.append({"state": "render_unverified",
                           "reason": ("Rendered DOM may still omit lazy or unvisited states."
                                      if render == "browser" else
                                      "Initial HTTP HTML may differ from the hydrated page.")})

    capture["id"] = save_capture(capture, raw, observations, network_responses, image_artifacts)

    payload = {
        "capture": capture,
        "observations": observations,
        "unresolved": unresolved,
        "extractor_views": {name: {"characters": len(output)} for name, output in views.items()},
        "extractors_unavailable": unavailable,
        "image_candidates": parser.images[:8],
        "saved_images": [{"sha256": _sha(image["bytes"]),
                          **{key: value for key, value in image.items() if key != "bytes"}}
                         for image in image_artifacts],
        "network_json_responses": [{key: value for key, value in response.items() if key != "json"}
                                   for response in network_responses],
        "purchase_controls": [button for button in parser.buttons
                              if re.search(r"buy|cart|purchase|অর্ডার", button["label"], re.IGNORECASE)][:8],
        "output_evidence_count": len(observations),
    }
    payload["resource_usage"] = {
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "html_bytes": len(raw),
        "image_bytes": sum(len(image["bytes"]) for image in image_artifacts),
        "network_json_bytes": sum(response.get("bytes", 0) for response in network_responses),
        "input_bytes": (len(raw) + sum(len(image["bytes"]) for image in image_artifacts) +
                        sum(response.get("bytes", 0) for response in network_responses)),
        "serialized_payload_bytes_excluding_usage": len(json.dumps(payload, ensure_ascii=False).encode("utf-8")),
    }
    return payload
