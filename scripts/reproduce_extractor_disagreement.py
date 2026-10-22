"""
Reproduction Experiment 1: Extractor Disagreement & Union Gain
==============================================================
Reference Literature: Li et al. (2026), "Beyond a Single Extractor: 
Re-thinking HTML-to-Text Extraction for LLM Pretraining", Findings of EACL 2026.

Objective:
Quantify the empirical information loss, disagreement, and union gain across 
multiple standard HTML-to-text extractors on real-world production web DOMs.
"""

import os
import sys
import time
import json
import re
from typing import Dict, List, Set, Tuple
from html.parser import HTMLParser

# Import extractors
import trafilatura
from readability import Document
import bs4
import html2text

# Import our AST Semantic Condenser from LWA-Web
sys.path.insert(0, os.path.abspath('.'))
from scripts.lightweight_web_extractor import ASTSemanticCondenser, LightweightWebExtractor

BENCHMARK_SITES = [
    {
        'id': 'BD-QC02',
        'name': 'Shwapno Online',
        'dom_path': 'data/stage-4/raw/bd-qc02-dom.html',
        'ground_truth': [
            ('Notification Heading', 'Get notifications from Shwapno?'),
            ('Value Pillar 1', '60 mins delivery'),
            ('Value Pillar 2', 'Authorized Products'),
            ('Value Pillar 3', 'Customer Service Support'),
            ('Value Pillar 4', 'Flexible Payments'),
            ('Egg Pricing', '12.75'),
            ('Alu Discount', '৳5 OFF'),
            ('Tea Deal Price', '95'),
            ('Brand Showcase', 'Refresh with Himalaya'),
            ('Dhaka Outlets', '290 outlets'),
            ('Gazipur Outlets', '69 outlets'),
            ('Support Hotline', '16469'),
            ('Support Email', 'queries@acilogistics.net'),
            ('Legal Entity', 'ACI SHWAPNO E-COMMERCE LIMITED'),
            ('Copyright Line', 'Copyright © 2026'),
            ('Trapped Coupon 1', 'PUJA6'),
            ('Trapped Coupon 2', 'PUJA7')
        ]
    },
    {
        'id': 'BD-FN02',
        'name': 'Nagad',
        'dom_path': 'data/stage-4/raw/bd-fn02-dom.html',
        'ground_truth': [
            ('Tagline', 'ডাক বিভাগের ডিজিটাল লেনদেন'),
            ('Active Lang', 'বাংলা'),
            ('Menu Link', 'নগদ ইসলামিক'),
            ('Hero Slogan', 'লেনদেন যেখানে নগদ সেখানে'),
            ('Section Heading', 'বর্তমান অফার'),
            ('Onboarding Step 1', 'এন আই ডি স্ক্যান করে'),
            ('Onboarding Step 3', '৪ ডিজিটের পিন'),
            ('Milestone Date', '২০১৯ সালের ২৬ মার্চ'),
            ('Milestone Scale', '৯ কোটির অধিক'),
            ('Hotline', '16181'),
            ('Copyright Line', '© 2026 Nagad'),
            ('App CTA', 'ডাউনলোড অ্যাপ'),
            ('Trapped Bonus Amount', '৳৮০'),
            ('Trapped Threshold', '৮,৮৮০')
        ]
    },
    {
        'id': 'BD-01',
        'name': 'Shohoz Bus',
        'dom_path': 'data/stage-4/raw/shohoz-bus-dom.html',
        'ground_truth': [
            ('Navbar Bus', 'Bus'),
            ('Navbar Air', 'Air'),
            ('Navbar Launch', 'Launch'),
            ('Helpline Number', '16374'),
            ('Support Email', 'info@shohoz.com'),
            ('Operating Hours', '7 AM - 11 PM'),
            ('Cancellation Policy', '12/24 hours'),
            ('Payment Channels', 'bKash'),
            ('Platform Scale Users', '10M+ users'),
            ('Platform Scale Tickets', '250M+ tickets'),
            ('Dynamic Unified Login Banner', 'Bus, Air, and Park with a single Shohoz account')
        ]
    },
    {
        'id': 'BD-02',
        'name': 'Chaldal',
        'dom_path': 'data/stage-4/raw/chaldal-dom.html',
        'ground_truth': [
            ('Default City', 'Dhaka'),
            ('Search Placeholder', 'Search for products'),
            ('Badge Products', '15000'),
            ('Badge Delivery', '1 hour'),
            ('Scale Warehouses', '26 warehouses'),
            ('Scale Orders', '5 million'),
            ('Scale Families', '100,000'),
            ('Delivery Hours', '7:30 AM'),
            ('Hotline', '16710'),
            ('Return Window', '7 days')
        ]
    }
]


def extract_with_trafilatura(html: str) -> str:
    res = trafilatura.extract(
        html,
        include_tables=True,
        include_links=True,
        include_images=True,
        favor_recall=True
    )
    return res or ""


def extract_with_readability(html: str) -> str:
    try:
        doc = Document(html)
        summary = doc.summary()
        soup = bs4.BeautifulSoup(summary, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return ""


def extract_with_bs4(html: str) -> str:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'svg', 'noscript']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)


def extract_with_html2text(html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    return h.handle(html)


def extract_with_lwa_condenser(html: str) -> str:
    condenser = ASTSemanticCondenser()
    condenser.feed(html)
    return condenser.get_condensed_markdown()


def compute_token_set(text: str) -> Set[str]:
    # Extract alpha-numeric tokens for Jaccard calculation
    tokens = re.findall(r'\b\w+\b', text.lower())
    return set(tokens)


def compute_jaccard(set_a: Set[str], set_b: Set[str]) -> float:
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def run_experiment():
    print("=" * 85)
    print("REPRODUCTION EXPERIMENT 1: EXTRACTOR DISAGREEMENT & UNION GAIN (Li et al., 2026)")
    print("=" * 85)

    all_results = {}

    for site in BENCHMARK_SITES:
        site_id = site['id']
        site_name = site['name']
        dom_path = site['dom_path']

        if not os.path.exists(dom_path):
            print(f"Skipping {site_name}: DOM file not found at {dom_path}")
            continue

        with open(dom_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        raw_bytes = len(html.encode('utf-8'))
        raw_tokens_est = raw_bytes // 4

        print(f"\n--- Site: {site_name} ({site_id}) ---")
        print(f"Raw DOM Size: {raw_bytes:,} bytes (~{raw_tokens_est:,} tokens)")

        # Run extractors with timing
        extractors = {}

        # 1. Trafilatura
        t0 = time.perf_counter()
        txt_trafilatura = extract_with_trafilatura(html)
        d_trafilatura = (time.perf_counter() - t0) * 1000.0
        extractors['Trafilatura'] = (txt_trafilatura, d_trafilatura)

        # 2. Readability
        t0 = time.perf_counter()
        txt_readability = extract_with_readability(html)
        d_readability = (time.perf_counter() - t0) * 1000.0
        extractors['Readability'] = (txt_readability, d_readability)

        # 3. BS4 get_text
        t0 = time.perf_counter()
        txt_bs4 = extract_with_bs4(html)
        d_bs4 = (time.perf_counter() - t0) * 1000.0
        extractors['BeautifulSoup4'] = (txt_bs4, d_bs4)

        # 4. html2text
        t0 = time.perf_counter()
        txt_html2text = extract_with_html2text(html)
        d_html2text = (time.perf_counter() - t0) * 1000.0
        extractors['html2text'] = (txt_html2text, d_html2text)

        # 5. LWA-Web Condenser
        t0 = time.perf_counter()
        txt_lwa = extract_with_lwa_condenser(html)
        d_lwa = (time.perf_counter() - t0) * 1000.0
        extractors['LWA-Web Condenser'] = (txt_lwa, d_lwa)

        # 6. Extractor Union (combining all distinct texts)
        txt_union = (
            f"# TRAFILATURA\n{txt_trafilatura}\n\n"
            f"# READABILITY\n{txt_readability}\n\n"
            f"# BS4\n{txt_bs4}\n\n"
            f"# HTML2TEXT\n{txt_html2text}\n\n"
            f"# LWA_CONDENSER\n{txt_lwa}"
        )
        extractors['Extractor Union'] = (txt_union, sum(e[1] for e in extractors.values()))

        # Evaluate Ground Truth Item Recall
        gt_items = site['ground_truth']
        total_gt = len(gt_items)
        scores = {}

        for ext_name, (ext_txt, ext_lat) in extractors.items():
            hits = 0
            missed = []
            for label, needle in gt_items:
                if needle.lower() in ext_txt.lower():
                    hits += 1
                else:
                    missed.append((label, needle))
            recall = (hits / total_gt) * 100.0
            chars = len(ext_txt)
            tokens_est = chars // 4
            reduction = (1.0 - (chars / raw_bytes)) * 100.0
            scores[ext_name] = {
                'hits': hits,
                'total': total_gt,
                'recall': recall,
                'chars': chars,
                'tokens_est': tokens_est,
                'token_reduction': reduction,
                'latency_ms': ext_lat,
                'missed': missed
            }

        # Print Comparative Table
        print(f"\nComparative Extractor Yield & Ground-Truth Recall ({site_name}):")
        print(f"{'Extractor':<20} | {'Chars':<9} | {'Tokens':<8} | {'Reduction':<10} | {'Latency':<9} | {'GT Recall':<15}")
        print("-" * 85)
        for ext_name, sc in scores.items():
            print(f"{ext_name:<20} | {sc['chars']:<9,} | {sc['tokens_est']:<8,} | {sc['token_reduction']:<9.1f}% | {sc['latency_ms']:<7.1f}ms | {sc['hits']}/{sc['total']} ({sc['recall']:.1f}%)")

        # Compute Extractor Disagreement Matrix (Jaccard token overlap)
        token_sets = {name: compute_token_set(text) for name, (text, _) in extractors.items() if name != 'Extractor Union'}
        ext_names_list = list(token_sets.keys())
        
        print("\nExtractor Vocabulary Overlap Matrix (Jaccard Similarity):")
        header = f"{'':<20} " + " ".join([f"{n[:8]:<9}" for n in ext_names_list])
        print(header)
        for name_a in ext_names_list:
            row = [f"{name_a[:19]:<20}"]
            for name_b in ext_names_list:
                jacc = compute_jaccard(token_sets[name_a], token_sets[name_b])
                row.append(f"{jacc:<9.2f}")
            print(" ".join(row))

        # Extractor Union Gain Analysis
        # Count facts captured by at least one extractor, and identify individual extractor blind spots
        single_best = max([sc['hits'] for k, sc in scores.items() if k != 'Extractor Union'])
        union_hits = scores['Extractor Union']['hits']
        union_gain = union_hits - single_best

        print(f"\nExtractor Union Gain on {site_name}:")
        print(f"  Single Best Extractor Score: {single_best}/{total_gt} ({single_best/total_gt*100:.1f}%)")
        print(f"  Extractor Union Score:       {union_hits}/{total_gt} ({union_hits/total_gt*100:.1f}%)")
        print(f"  Absolute Union Gain:         +{union_gain} ground-truth item(s) recovered via ensembling")

        all_results[site_id] = scores

    # Save complete JSON results
    out_path = "results/reproduced-extractor-disagreement-results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        # Convert non-serializable tuples
        serializable = {}
        for s_id, s_res in all_results.items():
            serializable[s_id] = {}
            for e_name, e_data in s_res.items():
                serializable[s_id][e_name] = {
                    'hits': e_data['hits'],
                    'total': e_data['total'],
                    'recall': e_data['recall'],
                    'chars': e_data['chars'],
                    'tokens_est': e_data['tokens_est'],
                    'token_reduction': e_data['token_reduction'],
                    'latency_ms': e_data['latency_ms'],
                    'missed_labels': [m[0] for m in e_data['missed']]
                }
        json.dump(serializable, f, indent=2)

    print(f"\nSaved complete benchmark results to: {out_path}")
    print("=" * 85)


if __name__ == '__main__':
    run_experiment()
