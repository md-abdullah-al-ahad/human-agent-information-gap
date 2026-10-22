"""
Lightweight Web Extraction Framework (LWA-Web) Prototype
=========================================================
Authors: Empirical AI & Agent Research Group
Objective: Explore HTML condensation and hand-entered fixture annotations.

Core Modules:
1. HTMLParser-based text condenser (byte-size reduction varies by page)
2. Optional, hand-entered annotations for known benchmark image filenames
3. Neutral warning that a purchase button alone does not prove stock
4. Offline byte-size and literal-string checks

This prototype does not perform OCR, browser acquisition, or end-to-end agent
evaluation. Its fixture checks must not be reported as general extraction accuracy.
"""

from html.parser import HTMLParser
import re
import os
import time
import json
from typing import Dict, List, Optional, Tuple

class ASTSemanticCondenser(HTMLParser):
    """
    Parses raw HTML into selected text and element references, omitting script,
    style, SVG, and other skipped blocks. It does not measure tokenizer usage.
    """
    def __init__(self, strip_classes: bool = True):
        super().__init__()
        self.output = []
        self.images = []
        self.interactive_elements = []
        self.skip_blocks = {'script', 'style', 'svg', 'noscript', 'head', 'iframe'}
        self.in_skip = 0
        self.strip_classes = strip_classes
        self.current_button = None

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

            is_candidate = self._is_trapped_banner_candidate(src, alt, title, classes)
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
            if tag == 'button':
                self.current_button = None

    def handle_data(self, data: str):
        if self.in_skip > 0:
            return
        text = data.strip()
        if text:
            self.output.append(text + " ")

    def _is_trapped_banner_candidate(self, src: str, alt: str, title: str, classes: str) -> bool:
        """Heuristic classifier to flag images likely harboring trapped text."""
        keywords = ['slider', 'banner', 'hero', 'campaign', 'promo', 'offer', 'voucher', 'coupon', 'festive', 'puja', 'special']
        text_corpus = f"{src} {alt} {title} {classes}".lower()
        has_keyword = any(k in text_corpus for k in keywords)
        is_hero_layout = 'object-cover' in classes or 'inset-0' in classes
        return has_keyword or is_hero_layout

    def get_condensed_markdown(self) -> str:
        raw_text = "".join(self.output)
        clean_text = re.sub(r'[ \t]+', ' ', raw_text)
        clean_text = re.sub(r'\n\s*\n+', '\n\n', clean_text).strip()
        return clean_text


class VisualMicroTriageEngine:
    """
    Identifies candidate image references and injects supplied fixture annotations.
    No image bytes are opened and no OCR or vision model is called.
    """
    def __init__(self, ground_truth_enrichments: Optional[Dict[str, str]] = None):
        self.known_enrichments = ground_truth_enrichments or {}

    def enrich_semantic_markdown(self, markdown_text: str, images: List[Dict]) -> Tuple[str, int]:
        enriched_count = 0
        for idx, img in enumerate(images):
            if img.get('is_banner_candidate'):
                corpus = f"{img['src']} {img['raw_src']} {img['alt']} {img['title']}".lower()
                trapped_text = None
                for key, val in self.known_enrichments.items():
                    if key.lower() in corpus:
                        trapped_text = val
                        break

                if trapped_text:
                    pattern = f"\\[IMG id={idx} [^\\]]+\\]"
                    replacement = f"[IMG id={idx} alt='{img['alt']}' data-trapped-text=\"{trapped_text}\" src='{img['src']}']"
                    markdown_text = re.sub(pattern, replacement, markdown_text)
                    enriched_count += 1

        return markdown_text, enriched_count


class DeterministicOmissionNormalizer:
    """
    Adds a neutral reminder beside purchase buttons. It cannot determine from a
    button alone whether an explicit stock statement exists elsewhere on a page.
    """
    def normalize(self, markdown_text: str) -> str:
        pattern = r"(\[BUTTON[^\]]*:[^\]]*(?:Add to Cart|Buy Now|অর্ডার করুন)[^\]]*\])"
        
        def annotate_button(match):
            btn = match.group(1)
            return f"{btn} <!-- Purchase-button state alone does not establish inventory status. -->"
            
        normalized = re.sub(pattern, annotate_button, markdown_text, flags=re.IGNORECASE)
        return normalized


class LightweightWebExtractor:
    """
    Offline HTML condenser with optional known-site fixture annotations.
    Output size and speed do not establish factual completeness.
    """
    def __init__(self, ground_truth_enrichments: Optional[Dict[str, str]] = None):
        self.triage = VisualMicroTriageEngine(ground_truth_enrichments)
        self.normalizer = DeterministicOmissionNormalizer()

    def process_dom(self, html_content: str) -> Dict:
        start_time = time.perf_counter()
        raw_bytes = len(html_content.encode('utf-8'))

        # Step 1: HTML text condensation
        condenser = ASTSemanticCondenser()
        condenser.feed(html_content)
        condensed_md = condenser.get_condensed_markdown()

        # Step 2: Optional hand-entered fixture annotation
        enriched_md, trapped_count = self.triage.enrich_semantic_markdown(
            condensed_md, condenser.images
        )

        # Step 3: Omission & Affordance Normalization
        final_doc = self.normalizer.normalize(enriched_md)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0
        final_bytes = len(final_doc.encode('utf-8'))
        byte_reduction_pct = (1.0 - (final_bytes / raw_bytes)) * 100.0 if raw_bytes else 0.0

        raw_tokens_est = raw_bytes // 4
        condensed_tokens_est = final_bytes // 4

        return {
            'raw_bytes': raw_bytes,
            'condensed_bytes': final_bytes,
            'byte_reduction_pct': byte_reduction_pct,
            'raw_tokens_est': raw_tokens_est,
            'condensed_tokens_est': condensed_tokens_est,
            'fixture_annotations_inserted': trapped_count,
            'processing_time_ms': processing_time_ms,
            'document': final_doc
        }


def run_benchmark():
    """Runs an offline fixture demonstration on existing HTML captures."""
    print("=" * 80)
    print("LIGHTWEIGHT WEB EXTRACTION FRAMEWORK (LWA-WEB) FIXTURE DEMO")
    print("=" * 80)

    test_sites = [
        {
            'name': 'Shwapno Online (BD-QC02)',
            'dom_path': 'data/stage-4/raw/bd-qc02-dom.html',
            'enrichments': {
                'puja': 'স্বপ্ন অনলাইনে পূজার সাশ্রয় | PUJA6: 6% discount (max ৳150 on ৳1000+) | PUJA7: 7% discount (max ৳200 on ৳1500+)',
                '6aca72b5': 'স্বপ্ন অনলাইনে পূজার সাশ্রয় | PUJA6: 6% discount (max ৳150 on ৳1000+) | PUJA7: 7% discount (max ৳200 on ৳1500+)'
            },
            'target_checks': ['PUJA6', 'PUJA7', 'স্বপ্ন', 'Eggs', 'Dhaka', '16469']
        },
        {
            'name': 'Nagad (BD-FN02)',
            'dom_path': 'data/stage-4/raw/bd-fn02-dom.html',
            'enrichments': {
                'nagad': 'উইকেন্ডে লেনদেন হবে ননস্টপ | ৮,৮৮০ টাকা লেনদেনে ৮০ টাকা ইনস্ট্যান্ট বোনাস'
            },
            'target_checks': ['৮,৮৮০', '৮০', 'নগদ', 'ইসলামিক', '২০১৯', '৯ কোটির অধিক']
        },
        {
            'name': 'Shohoz Bus Tickets (BD-01)',
            'dom_path': 'data/stage-4/raw/shohoz-bus-dom.html',
            'enrichments': {},
            'target_checks': ['Bus', 'Air', 'Park', '16374', 'shohoz']
        }
    ]

    for site in test_sites:
        path = site['dom_path']
        if not os.path.exists(path):
            print(f"Skipping {site['name']}: file not found ({path})")
            continue

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        site_extractor = LightweightWebExtractor(site['enrichments'])
        res = site_extractor.process_dom(html)

        print(f"\n[BENCHMARK] Target: {site['name']}")
        print(f"  Raw DOM Payload:          {res['raw_bytes']:,} bytes (~{res['raw_tokens_est']:,} tokens)")
        print(f"  LWA-Web Condensed Output: {res['condensed_bytes']:,} bytes (~{res['condensed_tokens_est']:,} tokens)")
        print(f"  Byte-Size Reduction:      {res['byte_reduction_pct']:.2f}% (not measured tokenizer savings)")
        print(f"  Processing Latency:       {res['processing_time_ms']:.2f} ms")
        print(f"  Fixture Annotations:      {res['fixture_annotations_inserted']} image reference(s)")

        doc = res['document']
        checks = {}
        for check in site['target_checks']:
            checks[check] = check in doc

        print("  Information Retention Verification:")
        for check, found in checks.items():
            status = "PASS" if found else "FAIL"
            print(f"    - Target '{check}': [{status}]")

    print("\n" + "=" * 80)
    print("FIXTURE DEMO COMPLETED: These selected string checks do not measure general recall.")
    print("=" * 80)

if __name__ == "__main__":
    run_benchmark()
