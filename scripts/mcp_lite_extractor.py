"""LWA-Web MCP server exposing source-linked evidence extraction.

The older ``extract_web_page`` fixture function remains importable for historical
reproduction but is not exposed to agents as an MCP tool.
"""

import os
import json
import sys
import time
import re
import urllib.request
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple
from html.parser import HTMLParser
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

try:
    from .lwa_evidence import inspect_page
    from .lwa_evidence_store import (inspect_evidence as read_saved_evidence,
                                     inspect_image_crop as read_saved_image_crop,
                                     check_claim as check_saved_claim,
                                     check_structured_claim as check_saved_structured_claim)
except ImportError:  # Direct execution: python scripts/mcp_lite_extractor.py
    from lwa_evidence import inspect_page
    from lwa_evidence_store import (inspect_evidence as read_saved_evidence,
                                    inspect_image_crop as read_saved_image_crop,
                                    check_claim as check_saved_claim,
                                    check_structured_claim as check_saved_structured_claim)

mcp = FastMCP("lite-web-extractor")
REPO_ROOT = Path(__file__).resolve().parents[1]

# Known benchmark cache mapping for explicitly requested offline evaluation.
BENCHMARK_CACHE = {
    'shwapno.com': 'data/stage-4/raw/bd-qc02-dom.html',
    'nagad.com.bd': 'data/stage-4/raw/bd-fn02-dom.html',
    'shohoz.com': 'data/stage-4/raw/shohoz-bus-dom.html',
    'chaldal.com': 'data/stage-4/raw/chaldal-dom.html',
    'bdjobs.com': 'data/stage-4/raw/bd-cl02-dom.html',
    'bikroy.com': 'data/stage-4/raw/bd-cl01-dom.html',
    '10minuteschool.com': 'data/stage-4/raw/bd-ed01-dom.html',
    'bangladesh.gov.bd': 'data/stage-4/raw/bd-gv01-dom.html',
    'usbair.com': 'data/stage-4/raw/bd-tr03-dom.html'
}


@mcp.tool()
def inspect_web_evidence(
    target: str,
    question: str = "",
    mode: str = "live",
    snapshot_captured_at_utc: Optional[str] = None,
    image_paths: Optional[List[str]] = None,
    render: str = "http",
) -> dict:
    """Return source-linked page evidence and unresolved states for an agent.

    Use mode='live' for an HTTP(S) URL or mode='snapshot' for a saved local HTML
    file. Snapshot mode never makes a network request. Image paths are optional
    saved local assets for OCR; unavailable OCR is reported, never invented.
    Set render='browser' in live mode to capture a bounded Chromium DOM. This
    does not guarantee that every lazy or interactive state was visited. The
    tool can fetch up to three referenced live-page raster assets for OCR when
    Tesseract is available. Snapshot OCR uses only caller-supplied image paths.
    """
    return inspect_page(target, question, mode, snapshot_captured_at_utc, image_paths, render)


@mcp.tool()
def inspect_evidence(capture_id: str, evidence_ids: List[str]) -> dict:
    """Retrieve exact saved observations and bounded source excerpts by capture handle."""
    return read_saved_evidence(capture_id, evidence_ids)


@mcp.tool()
def inspect_image_crop(
    capture_id: str, image_sha256: str, bbox: Optional[List[int]] = None,
) -> list:
    """View bounded saved pixels by capture/image hash and original-pixel bbox.

    Without bbox, a large image becomes an overview; request a bbox for legible
    text. The text block identifies the exact source and returned crop hash.
    """
    metadata, pixels = read_saved_image_crop(capture_id, image_sha256, bbox)
    return [json.dumps(metadata, ensure_ascii=False), Image(data=pixels, format="png")]


@mcp.tool()
def check_claim(capture_id: str, claim: str, evidence_ids: List[str]) -> dict:
    """Check literal quotation support; abstain on unverified semantic claims."""
    return check_saved_claim(capture_id, claim, evidence_ids)


@mcp.tool()
def check_structured_claim(
    capture_id: str, subject: str, predicate: str, expected_value: str,
    evidence_ids: List[str], object_name: str = "",
) -> dict:
    """Check explicit stock/compatibility wording for a named subject in cited HTML text.

    Supports or contradicts only the captured source statement, not real-world
    stock or physical compatibility. Unstated facts and OCR remain unresolved.
    """
    return check_saved_structured_claim(capture_id, subject, predicate,
                                        expected_value, evidence_ids, object_name)

# Hand-entered annotations for known benchmark assets; not OCR output.
VISUAL_ENRICHMENTS = {
    'shwapno': {
        'puja': 'স্বপ্ন অনলাইনে পূজার সাশ্রয় | PUJA6: 6% discount (max ৳150 on ৳1000+) | PUJA7: 7% discount (max ৳200 on ৳1500+)',
        '6aca72b5': 'স্বপ্ন অনলাইনে পূজার সাশ্রয় | PUJA6: 6% discount (max ৳150 on ৳1000+) | PUJA7: 7% discount (max ৳200 on ৳1500+)'
    },
    'nagad': {
        'nagad': 'উইকেন্ডে লেনদেন হবে ননস্টপ | ৮,৮৮০ টাকা লেনদেনে ৮০ টাকা ইনস্ট্যান্ট বোনাস'
    }
}


class ASTSemanticCondenser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.images = []
        self.skip_blocks = {'script', 'style', 'svg', 'noscript', 'head', 'iframe'}
        self.in_skip = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]):
        attr_dict = dict(attrs)
        if tag in self.skip_blocks:
            self.in_skip += 1
            return
        if self.in_skip > 0:
            return

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag in ['p', 'section', 'article', 'tr']:
            self.output.append("\n")
        elif tag == 'li':
            self.output.append("\n- ")
        elif tag == 'td' or tag == 'th':
            self.output.append(" | ")
        elif tag == 'button':
            cls = attr_dict.get('class', '')
            aria = attr_dict.get('aria-label', '')
            attrs_str = ""
            if cls:
                attrs_str += f" class='{cls}'"
            if aria:
                attrs_str += f" aria='{aria}'"
            self.output.append(f"\n[BUTTON{attrs_str}: ")
        elif tag == 'a':
            href = attr_dict.get('href', '')
            clean_href = href.split('?')[0] if '?' in href else href
            self.output.append(f" [LINK({clean_href}): ")
        elif tag == 'input':
            val = attr_dict.get('value', '') or attr_dict.get('placeholder', '')
            itype = attr_dict.get('type', 'text')
            self.output.append(f" [INPUT type='{itype}' val='{val}'] ")
        elif tag == 'img':
            src = attr_dict.get('src', '') or attr_dict.get('data-src', '')
            alt = attr_dict.get('alt', '').strip()
            title = attr_dict.get('title', '').strip()
            classes = attr_dict.get('class', '')

            if src.startswith('data:'):
                clean_src = '[INLINE_BASE64]'
            else:
                clean_src = src.split('?')[0] if '?' in src else src

            is_candidate = self._is_banner_candidate(src, alt, title, classes)
            img_entry = {
                'src': clean_src,
                'raw_src': src,
                'alt': alt,
                'title': title,
                'is_banner_candidate': is_candidate
            }
            self.images.append(img_entry)
            tag_id = len(self.images) - 1
            self.output.append(f" [IMG id={tag_id} alt='{alt}' title='{title}' src='{clean_src}'] ")

    def handle_endtag(self, tag: str):
        if tag in self.skip_blocks:
            if self.in_skip > 0:
                self.in_skip -= 1
            return
        if self.in_skip > 0:
            return

        if tag in ['button', 'a']:
            self.output.append("] ")

    def handle_data(self, data: str):
        if self.in_skip > 0:
            return
        text = data.strip()
        if text:
            self.output.append(text + " ")

    def _is_banner_candidate(self, src: str, alt: str, title: str, classes: str) -> bool:
        keywords = ['slider', 'banner', 'hero', 'campaign', 'promo', 'offer', 'voucher', 'coupon', 'festive', 'puja', 'special']
        text_corpus = f"{src} {alt} {title} {classes}".lower()
        return any(k in text_corpus for k in keywords) or 'object-cover' in classes or 'inset-0' in classes

    def get_condensed_markdown(self) -> str:
        raw_text = "".join(self.output)
        clean_text = re.sub(r'[ \t]+', ' ', raw_text)
        clean_text = re.sub(r'\n\s*\n+', '\n\n', clean_text).strip()
        return clean_text


def extract_web_page(target: str, use_benchmark_cache: bool = False) -> str:
    """
    Legacy static condensation fixture, deliberately not registered as an MCP
    tool. Its optional benchmark cache and known-image annotations are manually
    supplied; this function does not render pages or perform OCR.

    Args:
        target: Full HTTP(S) URL or local HTML file path.
        use_benchmark_cache: Serve a saved DOM for known domains only when True.
    """
    start_time = time.perf_counter()
    html_content = ""
    source_label = target

    # 1. Resolve source (Benchmark Cache, Local File, or Live HTTP fetch)
    matched_cache = None
    using_saved_cache = False
    if use_benchmark_cache and target.startswith(('http://', 'https://')):
        host = (urlparse(target).hostname or '').lower()
        for domain, path in BENCHMARK_CACHE.items():
            if host == domain or host.endswith('.' + domain):
                matched_cache = path
                break

    if matched_cache and (REPO_ROOT / matched_cache).exists():
        with (REPO_ROOT / matched_cache).open('r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        source_label = f"{target} (saved benchmark DOM: {matched_cache})"
        using_saved_cache = True
    elif os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        source_label = f"Local file: {target}"
    elif target.startswith(('http://', 'https://')):
        req = urllib.request.Request(
            target,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        source_label = f"Live HTTP GET: {target}"
    else:
        return f"Error: Unable to locate or fetch target '{target}'. Ensure it is a valid URL or existing file path."

    raw_bytes = len(html_content.encode('utf-8'))

    # 2. HTML text condensation
    condenser = ASTSemanticCondenser()
    condenser.feed(html_content)
    condensed_md = condenser.get_condensed_markdown()

    # 3. Inject known benchmark annotations; no pixels are inspected.
    site_enrichments = {}
    if using_saved_cache:
        for site_key, enrich_dict in VISUAL_ENRICHMENTS.items():
            if site_key in matched_cache.lower():
                site_enrichments = enrich_dict
                break

    enriched_count = 0
    for idx, img in enumerate(condenser.images):
        if img.get('is_banner_candidate'):
            corpus = f"{img['src']} {img['raw_src']} {img['alt']} {img['title']}".lower()
            trapped_text = None
            for key, val in site_enrichments.items():
                if key.lower() in corpus:
                    trapped_text = val
                    break
            if trapped_text:
                pattern = f"\\[IMG id={idx} [^\\]]+\\]"
                replacement = f"[IMG id={idx} alt='{img['alt']}' data-trapped-text=\"{trapped_text}\" src='{img['src']}']"
                condensed_md = re.sub(pattern, replacement, condensed_md)
                enriched_count += 1

    # 4. Deterministic Omission & Affordance Normalization
    pattern = r"(\[BUTTON[^\]]*:[^\]]*(?:Add to Cart|Buy Now|অর্ডার করুন)[^\]]*\])"
    def annotate_button(match):
        btn = match.group(1)
        return f"{btn} <!-- Purchase-button state alone does not establish inventory status. -->"
    final_doc = re.sub(pattern, annotate_button, condensed_md, flags=re.IGNORECASE)

    # 5. Performance Metrics
    duration_ms = (time.perf_counter() - start_time) * 1000.0
    final_bytes = len(final_doc.encode('utf-8'))
    reduction_pct = (1.0 - (final_bytes / raw_bytes)) * 100.0 if raw_bytes else 0.0

    header = (
        f"=== LWA-WEB MCP EXTRACTION REPORT ===\n"
        f"Source: {source_label}\n"
        f"Raw DOM Size: {raw_bytes:,} bytes (bytes/4 proxy: {raw_bytes//4:,})\n"
        f"Condensed Output: {final_bytes:,} bytes (bytes/4 proxy: {final_bytes//4:,})\n"
        f"Byte-Size Reduction: {reduction_pct:.2f}% (token count estimated as bytes/4)\n"
        f"Processing Time: {duration_ms:.2f} ms\n"
        f"Known-Asset Fixture Annotations: {enriched_count}\n"
        f"=====================================\n\n"
    )

    return header + final_doc


if __name__ == "__main__":
    mcp.run()
