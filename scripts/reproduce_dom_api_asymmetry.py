"""
Reproduction Experiment 2: DOM vs. Shadow API Asymmetry
======================================================
Reference Literature:
1. Song et al. (2025), "Beyond Browsing: API-Based Web Agents", Findings of ACL 2025.
2. Tham et al. (2026), "Internal APIs Are All You Need: Shadow APIs, Shared Discovery, 
   and the Case Against Browser-First Agent Architectures".

Objective:
Quantify the empirical information asymmetry, payload divergence, and retrieval efficiency
between the public rendered HTML DOM and internal/shadow backend APIs on production SPAs.
"""

import os
import sys
import time
import json
import re
import urllib.request
from typing import Dict, List, Any

# Target 1: Shwapno Algolia Production Search Index
ALGOLIA_APP_ID = "S2O8A9M97P"
ALGOLIA_API_KEY = "4ccf1b901eb824fb4a2a11375a3b14e0"
ALGOLIA_URL = f"https://{ALGOLIA_APP_ID.lower()}-dsn.algolia.net/1/indexes/Position/query"

SHWAPNO_PRODUCTS = [
    'Egg Loose',
    'Alu (Potato)',
    'ACI Pure Salt',
    'Masala Tea'
]

SHWAPNO_DOM_PATH = "data/stage-4/raw/bd-qc02-dom.html"
CHALDAL_DOM_PATH = "data/stage-4/raw/chaldal-dom.html"


def query_algolia(query_str: str) -> Dict[str, Any]:
    headers = {
        'X-Algolia-Application-Id': ALGOLIA_APP_ID,
        'X-Algolia-API-Key': ALGOLIA_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({'params': f"query={query_str}&hitsPerPage=1"}).encode('utf-8')
    req = urllib.request.Request(ALGOLIA_URL, data=payload, headers=headers)
    
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
    latency_ms = (time.perf_counter() - t0) * 1000.0
    
    hit = res['hits'][0] if res.get('hits') else {}
    return {
        'hit': hit,
        'latency_ms': latency_ms,
        'raw_response_bytes': len(json.dumps(hit).encode('utf-8'))
    }


def analyze_shwapno_asymmetry():
    print("=" * 85)
    print("TARGET 1: SHWAPNO ONLINE (BD-QC02) — DOM vs. ALGOLIA SHADOW API")
    print("=" * 85)
    
    with open(SHWAPNO_DOM_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        dom_text = f.read()
    
    dom_size_bytes = len(dom_text.encode('utf-8'))
    print(f"Rendered HTML DOM Size: {dom_size_bytes:,} bytes (~{dom_size_bytes//4:,} tokens)")
    
    results = []
    
    for prod_name in SHWAPNO_PRODUCTS:
        api_res = query_algolia(prod_name)
        hit = api_res['hit']
        if not hit:
            print(f"Product not found in Algolia: {prod_name}")
            continue
            
        api_fields = list(hit.keys())
        total_fields = len(api_fields)
        
        # Check which API fields exist in the DOM text
        present_in_dom = []
        omitted_from_dom = []
        
        for k, v in hit.items():
            if k in ['_highlightResult', 'ProductPictures']:
                continue
            val_str = str(v).strip()
            if not val_str or val_str in ['0', 'None', '[]', '{}']:
                continue
            # Search if value is in DOM
            if val_str in dom_text:
                present_in_dom.append((k, val_str[:40]))
            else:
                omitted_from_dom.append((k, val_str[:40]))
                
        asymmetry_ratio = (len(omitted_from_dom) / (len(present_in_dom) + len(omitted_from_dom))) * 100.0
        
        res_entry = {
            'product': hit.get('Name', prod_name),
            'id': hit.get('Id'),
            'price': hit.get('Price'),
            'total_quantity_sold': hit.get('TotalQuantitySold'),
            'api_latency_ms': api_res['latency_ms'],
            'api_payload_bytes': api_res['raw_response_bytes'],
            'total_tested_fields': len(present_in_dom) + len(omitted_from_dom),
            'present_in_dom_count': len(present_in_dom),
            'omitted_from_dom_count': len(omitted_from_dom),
            'asymmetry_ratio': asymmetry_ratio,
            'omitted_samples': omitted_from_dom[:5]
        }
        results.append(res_entry)
        
        print(f"\nProduct: {res_entry['product']} (ID: {res_entry['id']})")
        print(f"  Algolia API Latency:      {res_entry['api_latency_ms']:.2f} ms")
        print(f"  API Payload Size:         {res_entry['api_payload_bytes']} bytes (~{res_entry['api_payload_bytes']//4} tokens)")
        print(f"  Payload Size Reduction:   {100.0 - (res_entry['api_payload_bytes'] / dom_size_bytes * 100.0):.4f}% vs HTML DOM")
        print(f"  DOM Field Retention:      {res_entry['present_in_dom_count']}/{res_entry['total_tested_fields']} fields visible in DOM")
        print(f"  DOM Information Omission: {res_entry['omitted_from_dom_count']}/{res_entry['total_tested_fields']} fields ({asymmetry_ratio:.1f}% OMISSION)")
        print(f"  Critical Hidden Fields in Shadow API:")
        for k, v in res_entry['omitted_samples']:
            print(f"    - {k}: {v}")
            
    return results


def analyze_chaldal_asymmetry():
    print("\n" + "=" * 85)
    print("TARGET 2: CHALDAL (BD-02) — RENDERED DOM vs. EMBEDDED JSON STATE DICTIONARY")
    print("=" * 85)
    
    with open(CHALDAL_DOM_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        dom_text = f.read()
        
    dom_size_bytes = len(dom_text.encode('utf-8'))
    print(f"Rendered HTML DOM Size: {dom_size_bytes:,} bytes (~{dom_size_bytes//4:,} tokens)")
    
    # Extract window.__serviceState
    idx = dom_text.find('window.__serviceState = ')
    end_idx = dom_text.find('</script>', idx)
    json_str = dom_text[idx + len('window.__serviceState = '):end_idx]
    
    t0 = time.perf_counter()
    state_data = json.loads(json_str)
    parse_latency_ms = (time.perf_counter() - t0) * 1000.0
    
    json_bytes = len(json_str.encode('utf-8'))
    print(f"Embedded State JSON Size: {json_bytes:,} bytes (~{json_bytes//4:,} tokens)")
    print(f"JSON Parsing Time:        {parse_latency_ms:.2f} ms")
    
    # Analyze Category Service Asymmetry
    cats = state_data['CategoryService']['categories']['1']
    total_cats_in_state = len(cats)
    
    # Count how many category IDs/names are rendered in DOM text vs hidden
    rendered_cat_names = 0
    hidden_cat_ids = 0
    for c in cats:
        c_name = c['Name'].strip()
        c_id = str(c['Id'])
        if c_name in dom_text:
            rendered_cat_names += 1
        if c_id not in dom_text:
            hidden_cat_ids += 1
            
    # Analyze Marketing Banner Asymmetry
    banner_slots = state_data['MarketingService']['marketingBanner']
    total_banners = sum(len(v) if isinstance(v, list) else 1 for v in banner_slots.values())
    
    # Inspect scheduled timestamps
    sample_banner = banner_slots['33'][0] if '33' in banner_slots and banner_slots['33'] else {}
    start_time = sample_banner.get('StartTime')
    end_time = sample_banner.get('EndTime')
    banner_url = sample_banner.get('BannerUrl')
    
    # Check Cloudflare Email Obfuscation
    cf_email_masked = "[email\xa0protected]" in dom_text or "data-cfemail" in dom_text
    
    print(f"\nStructural Asymmetry Metrics (Chaldal):")
    print(f"  Total Hierarchical Categories in State:  {total_cats_in_state} categories")
    print(f"  Categories Rendered in Visible DOM:      {rendered_cat_names} categories")
    print(f"  Category Internal IDs Hidden from DOM:   {hidden_cat_ids}/{total_cats_in_state} ({hidden_cat_ids/total_cats_in_state*100:.1f}% hidden)")
    print(f"  Marketing Banners with Start/End Time:   {total_banners} banners across {len(banner_slots)} slots")
    print(f"  Sample Banner Metadata in Shadow State:  Target: {banner_url} (Active: {start_time} to {end_time})")
    print(f"  Cloudflare Anti-Bot Masking Active:      {'YES (data-cfemail XOR encryption)' if cf_email_masked else 'NO'}")
    
    return {
        'total_categories_state': total_cats_in_state,
        'rendered_categories_dom': rendered_cat_names,
        'hidden_cat_ids_ratio': (hidden_cat_ids / total_cats_in_state) * 100.0,
        'total_banners_state': total_banners,
        'cf_email_obfuscated': cf_email_masked
    }


def main():
    shwapno_results = analyze_shwapno_asymmetry()
    chaldal_results = analyze_chaldal_asymmetry()
    
    # Save combined report
    output_path = "results/reproduced-dom-api-asymmetry-results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            'shwapno_algolia_asymmetry': shwapno_results,
            'chaldal_state_asymmetry': chaldal_results
        }, f, indent=2)
        
    print("\n" + "=" * 85)
    print(f"Saved complete DOM vs. Shadow API Asymmetry results to: {output_path}")
    print("=" * 85)


if __name__ == '__main__':
    main()
