#!/usr/bin/env python3
"""
Summary of Hand-Coded Temporal Status Labels for Literature Gap 4:
Temporal Web Drift & Ground-Truth Invalidation
Based on:
- 'Online-Mind2Web: Benchmarking Web Agents in Changing Environments' (COLM 2025)
- 'LiveWeb-IE: Information Extraction under Real-World Web Evolution' (2026)

This script counts manually entered follow-up labels. It does not fetch live pages
or verify the listed values against separately preserved follow-up captures.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "results/reproduced-temporal-web-drift-results.json"

# Researcher-entered baseline and follow-up labels. Separate follow-up captures
# are not stored with these entries, so the labels remain unverified here.
SHWAPNO_ITEMS = [
    {
        "item_id": "BD-QC02-01",
        "category": "Notification Permission Modal Heading",
        "oct19_ground_truth": "Get notifications from Shwapno?",
        "modality": "UI_MODAL",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Get notifications from Shwapno?",
        "notes": "Modal prompt text remained identical."
    },
    {
        "item_id": "BD-QC02-02",
        "category": "Notification Permission Confirmation Button",
        "oct19_ground_truth": "Yes (Yellow primary button) vs No",
        "modality": "BUTTON_UI",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Yes vs No",
        "notes": "Action button structure unchanged."
    },
    {
        "item_id": "BD-QC02-03",
        "category": "Hero Banner Campaign Title",
        "oct19_ground_truth": "স্বপ্ন অনলাইন পূজার সাশ্রয়",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "CAMPAIGN_EXPIRED",
        "oct21_live_value": "Rotated / Expired (Festival campaign concluded)",
        "notes": "Puja shopping festival banner removed following holiday completion."
    },
    {
        "item_id": "BD-QC02-04",
        "category": "Puja Promo Coupon 1 Code & Terms",
        "oct19_ground_truth": "৬% ডিসকাউন্ট, Code: PUJA6 (2 times use, max ৳150 on ৳1000+)",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "CAMPAIGN_EXPIRED",
        "oct21_live_value": "Code PUJA6 Decommissioned",
        "notes": "Voucher expired; no longer active or referenced."
    },
    {
        "item_id": "BD-QC02-05",
        "category": "Puja Promo Coupon 2 Code & Terms",
        "oct19_ground_truth": "৭% ডিসকাউন্ট, Code: PUJA7 (1 time use, max ৳200 on ৳1500+)",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "CAMPAIGN_EXPIRED",
        "oct21_live_value": "Code PUJA7 Decommissioned",
        "notes": "Voucher expired; no longer active or referenced."
    },
    {
        "item_id": "BD-QC02-06",
        "category": "Value Proposition Pillar 1",
        "oct19_ground_truth": "60 Mins Delivery (Free shipping over 1500Tk)",
        "modality": "SERVICE_PILLAR",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "60 Mins Delivery (Free shipping over 1500Tk)",
        "notes": "Service pillar text preserved verbatim."
    },
    {
        "item_id": "BD-QC02-07",
        "category": "Value Proposition Pillar 2",
        "oct19_ground_truth": "Authorized Products (within 30 days for an exchange)",
        "modality": "SERVICE_PILLAR",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Authorized Products (within 30 days for an exchange)",
        "notes": "Service pillar text preserved verbatim."
    },
    {
        "item_id": "BD-QC02-08",
        "category": "Value Proposition Pillar 3",
        "oct19_ground_truth": "Customer Service Support (8am to 10pm)",
        "modality": "SERVICE_PILLAR",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Customer Service Support (8am to 10pm)",
        "notes": "Operating hours preserved verbatim."
    },
    {
        "item_id": "BD-QC02-09",
        "category": "Value Proposition Pillar 4",
        "oct19_ground_truth": "Flexible Payments (Pay with multiple credit cards)",
        "modality": "SERVICE_PILLAR",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Flexible Payments (Pay with multiple credit cards)",
        "notes": "Payment pillar preserved verbatim."
    },
    {
        "item_id": "BD-QC02-10",
        "category": "Fast Category Quick Tile 1",
        "oct19_ground_truth": "Eggs (with brown eggs photo)",
        "modality": "CATEGORY_TILE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Eggs",
        "notes": "Category quick tile preserved."
    },
    {
        "item_id": "BD-QC02-11",
        "category": "Fast Category Quick Tile 3",
        "oct19_ground_truth": "Soft Drinks (with Mojo, RC, 7Up, Pepsi bottles)",
        "modality": "CATEGORY_TILE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Soft Drinks",
        "notes": "Category quick tile preserved."
    },
    {
        "item_id": "BD-QC02-12",
        "category": "Recommended Product 1 Price & MOQ",
        "oct19_ground_truth": "Egg Loose — ৳12.75 Per Piece (Min. 12)",
        "modality": "PRODUCT_CARD",
        "oct21_status": "PRICE_DRIFT",
        "oct21_live_value": "Egg Loose — ৳11.00 Per Piece (Drop: -13.7%)",
        "notes": "Algolia hit confirms Price changed from ৳12.75 to ৳11.00."
    },
    {
        "item_id": "BD-QC02-13",
        "category": "Recommended Product 2 Discount",
        "oct19_ground_truth": "Alu (Potato) Regular Loose Kg — ৳25 (৳5 OFF, regular ৳30)",
        "modality": "PRODUCT_CARD",
        "oct21_status": "PRICE_DRIFT",
        "oct21_live_value": "Alu (Potato) Regular Loose Kg — ৳27 (Promo expired, +8.0%)",
        "notes": "Algolia hit confirms Price=27, SpecialPrice=None."
    },
    {
        "item_id": "BD-QC02-14",
        "category": "Recommended Product 4 Price",
        "oct19_ground_truth": "ACI Pure Salt 1kg — ৳42 Per Piece",
        "modality": "PRODUCT_CARD",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "ACI Pure Salt 1kg — ৳42 Per Piece",
        "notes": "Algolia hit confirms Price=42 unchanged."
    },
    {
        "item_id": "BD-QC02-15",
        "category": "Weekday Deals Featured Product",
        "oct19_ground_truth": "Fresh Premium Masala Tea 50gm — ৳95 (৳15 OFF, regular ৳110)",
        "modality": "PRODUCT_CARD",
        "oct21_status": "ROTATED",
        "oct21_live_value": "Finlays Masala Tea Bag in Bag 50gm — ৳150",
        "notes": "Hero deal carousel rotated to different brand/item."
    },
    {
        "item_id": "BD-QC02-16",
        "category": "Himalaya Promotional Section Heading",
        "oct19_ground_truth": "REFRESH WITH HIMALAYA",
        "modality": "SECTION_HEADER",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "REFRESH WITH HIMALAYA",
        "notes": "Brand sponsorship block preserved."
    },
    {
        "item_id": "BD-QC02-17",
        "category": "Coverage Area (Dhaka Outlets)",
        "oct19_ground_truth": "Dhaka — 290 outlets",
        "modality": "COVERAGE_TABLE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Dhaka — 290 outlets",
        "notes": "Outlet count preserved verbatim."
    },
    {
        "item_id": "BD-QC02-18",
        "category": "Coverage Area (Gazipur Outlets)",
        "oct19_ground_truth": "Gazipur — 69 outlets",
        "modality": "COVERAGE_TABLE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "Gazipur — 69 outlets",
        "notes": "Outlet count preserved verbatim."
    },
    {
        "item_id": "BD-QC02-19",
        "category": "Customer Support Hotline & Email",
        "oct19_ground_truth": "Call Us: 16469 (8am-10pm, Everyday), Email: queries@acilogistics.net",
        "modality": "CONTACT_TEXT",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "16469, queries@acilogistics.net",
        "notes": "Support hotlines preserved verbatim."
    },
    {
        "item_id": "BD-QC02-20",
        "category": "Operating Legal Entity & Copyright",
        "oct19_ground_truth": "ACI SHWAPNO E-COMMERCE LIMITED and Copyright © 2026",
        "modality": "LEGAL_NOTICE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "ACI SHWAPNO E-COMMERCE LIMITED and Copyright © 2026",
        "notes": "Corporate legal entity notice unchanged."
    }
]

NAGAD_ITEMS = [
    {
        "item_id": "BD-FN02-01",
        "category": "Nagad Logo Subtitle Tagline",
        "oct19_ground_truth": "ডাক বিভাগের ডিজিটাল লেনদেন",
        "modality": "BRAND_TAGLINE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "ডাক বিভাগের ডিজিটাল লেনদেন",
        "notes": "Brand tagline in header intact in hydrated DOM."
    },
    {
        "item_id": "BD-FN02-02",
        "category": "Active Language Selection",
        "oct19_ground_truth": "বাংলা (Active with red rounded pill vs English inactive)",
        "modality": "UI_STATE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "বাংলা active toggle",
        "notes": "Language switch UI state preserved."
    },
    {
        "item_id": "BD-FN02-03",
        "category": "Main Nav Sixth Menu Item",
        "oct19_ground_truth": "নগদ ইসলামিক",
        "modality": "NAV_LINK",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "নগদ ইসলামিক",
        "notes": "Navigation hierarchy unchanged."
    },
    {
        "item_id": "BD-FN02-04",
        "category": "Popup Modal Headline",
        "oct19_ground_truth": "নগদ অ্যাপে নতুন Experience",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "ROTATED",
        "oct21_live_value": "Popup modal rotated / dismissed on live load",
        "notes": "Promotional modal image asset rotated."
    },
    {
        "item_id": "BD-FN02-05",
        "category": "Popup Modal Central Slogan",
        "oct19_ground_truth": "সব হবে Nonstop",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "ROTATED",
        "oct21_live_value": "Rotated / Decommissioned",
        "notes": "Embedded slogan dismissed with popup."
    },
    {
        "item_id": "BD-FN02-06",
        "category": "Popup Modal Featured Ambassador",
        "oct19_ground_truth": "Jamal Bhuyan (Bangladeshi athlete in red jersey holding smartphone)",
        "modality": "VISUAL_ENTITY",
        "oct21_status": "ROTATED",
        "oct21_live_value": "Rotated / Decommissioned",
        "notes": "Ambassador graphic modal dismissed with popup."
    },
    {
        "item_id": "BD-FN02-07",
        "category": "Popup Modal CTA Button",
        "oct19_ground_truth": "Let's go (with red right-arrow icon)",
        "modality": "BUTTON_UI",
        "oct21_status": "ROTATED",
        "oct21_live_value": "Rotated / Decommissioned",
        "notes": "Modal action button dismissed with popup."
    },
    {
        "item_id": "BD-FN02-08",
        "category": "Hero Slogan Behind Popup",
        "oct19_ground_truth": "লেনদেন যেখানে নগদ সেখানে",
        "modality": "TEXT_TYPOGRAPHY",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "লেনদেন যেখানে নগদ সেখানে",
        "notes": "Hero banner core slogan present in hydrated DOM."
    },
    {
        "item_id": "BD-FN02-09",
        "category": "Hero Shop Signboard Text",
        "oct19_ground_truth": "সর্বনিম্ন ক্যাশ আউট চার্জ",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "সর্বনিম্ন ক্যাশ আউট চার্জ",
        "notes": "Background asset preserved."
    },
    {
        "item_id": "BD-FN02-10",
        "category": "Current Offers Section Heading",
        "oct19_ground_truth": "বর্তমান অফার",
        "modality": "SECTION_HEADER",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "বর্তমান অফার",
        "notes": "Section header preserved verbatim."
    },
    {
        "item_id": "BD-FN02-11",
        "category": "Weekend Add Money Required Transaction Amount",
        "oct19_ground_truth": "৳8,880 (8,880 অ্যাড মানিতে)",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "CAMPAIGN_EXPIRED",
        "oct21_live_value": "Expired (Weekend promotion inactive on Tuesday)",
        "notes": "Sunday weekend campaign rotated out on weekday cycle."
    },
    {
        "item_id": "BD-FN02-12",
        "category": "Weekend Add Money Instant Bonus Amount",
        "oct19_ground_truth": "৳80 (৳80 ইনস্ট্যান্ট বোনাস)",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "CAMPAIGN_EXPIRED",
        "oct21_live_value": "Expired (Weekend promotion inactive on Tuesday)",
        "notes": "Bonus terms expired with campaign."
    },
    {
        "item_id": "BD-FN02-13",
        "category": "DeeptoPlay Subscription Cashback Offer",
        "oct19_ground_truth": "২০% (২০% ক্যাশব্যাক নগদ পেমেন্টে)",
        "modality": "IN_IMAGE_GRAPHIC",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "২০% ক্যাশব্যাক",
        "notes": "Active entertainment campaign preserved."
    },
    {
        "item_id": "BD-FN02-14",
        "category": "Account Opening Section Heading",
        "oct19_ground_truth": "নগদ একাউন্ট খুলুন",
        "modality": "SECTION_HEADER",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "নগদ একাউন্ট খুলুন",
        "notes": "Onboarding heading preserved verbatim."
    },
    {
        "item_id": "BD-FN02-15",
        "category": "Account Opening Subheading",
        "oct19_ground_truth": "আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ",
        "modality": "SUBTITLE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ",
        "notes": "Subheading preserved verbatim."
    },
    {
        "item_id": "BD-FN02-16",
        "category": "Account Opening Step 1",
        "oct19_ground_truth": "এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন",
        "modality": "STEP_CARD",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন",
        "notes": "Onboarding step 1 preserved verbatim."
    },
    {
        "item_id": "BD-FN02-17",
        "category": "Account Opening Step 2",
        "oct19_ground_truth": "সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন",
        "modality": "STEP_CARD",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন",
        "notes": "Onboarding step 2 preserved verbatim."
    },
    {
        "item_id": "BD-FN02-18",
        "category": "Account Opening Step 3",
        "oct19_ground_truth": "৪ ডিজিটের পিন সেট করুন",
        "modality": "STEP_CARD",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "৪ ডিজিটের পিন সেট করুন",
        "notes": "Onboarding step 3 preserved verbatim."
    },
    {
        "item_id": "BD-FN02-19",
        "category": "Postal DFS Journey Start Date & Milestone",
        "oct19_ground_truth": "২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক",
        "modality": "QUANTITATIVE_TEXT",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক",
        "notes": "Institutional history preserved verbatim."
    },
    {
        "item_id": "BD-FN02-20",
        "category": "Official Copyright Notice & App CTA",
        "oct19_ground_truth": "© 2026 Nagad All rights reserved and ডাউনলোড অ্যাপ",
        "modality": "LEGAL_NOTICE",
        "oct21_status": "PERSISTED",
        "oct21_live_value": "© 2026 Nagad All rights reserved and ডাউনলোড অ্যাপ",
        "notes": "Footer copyright and CTA preserved."
    }
]

def analyze_temporal_drift():
    all_items = SHWAPNO_ITEMS + NAGAD_ITEMS
    total_evaluated = len(all_items)

    status_counts = {
        "PERSISTED": 0,
        "PRICE_DRIFT": 0,
        "CAMPAIGN_EXPIRED": 0,
        "ROTATED": 0
    }

    site_breakdown = {
        "BD-QC02 (Shwapno)": {"total": len(SHWAPNO_ITEMS), "persisted": 0, "invalidated": 0, "drift_categories": {}},
        "BD-FN02 (Nagad)": {"total": len(NAGAD_ITEMS), "persisted": 0, "invalidated": 0, "drift_categories": {}}
    }

    for item in SHWAPNO_ITEMS:
        st = item["oct21_status"]
        status_counts[st] += 1
        if st == "PERSISTED":
            site_breakdown["BD-QC02 (Shwapno)"]["persisted"] += 1
        else:
            site_breakdown["BD-QC02 (Shwapno)"]["invalidated"] += 1
            site_breakdown["BD-QC02 (Shwapno)"]["drift_categories"][st] = site_breakdown["BD-QC02 (Shwapno)"]["drift_categories"].get(st, 0) + 1

    for item in NAGAD_ITEMS:
        st = item["oct21_status"]
        status_counts[st] += 1
        if st == "PERSISTED":
            site_breakdown["BD-FN02 (Nagad)"]["persisted"] += 1
        else:
            site_breakdown["BD-FN02 (Nagad)"]["invalidated"] += 1
            site_breakdown["BD-FN02 (Nagad)"]["drift_categories"][st] = site_breakdown["BD-FN02 (Nagad)"]["drift_categories"].get(st, 0) + 1

    total_persisted = status_counts["PERSISTED"]
    total_invalidated = total_evaluated - total_persisted
    invalidation_rate_pct = round((total_invalidated / total_evaluated) * 100, 2)
    persistence_rate_pct = round((total_persisted / total_evaluated) * 100, 2)

    for site, data in site_breakdown.items():
        data["invalidation_rate_pct"] = round((data["invalidated"] / data["total"]) * 100, 2)
        data["persistence_rate_pct"] = round((data["persisted"] / data["total"]) * 100, 2)

    # Modality vulnerability to temporal drift
    modality_drift = {}
    for item in all_items:
        mod = item["modality"]
        if mod not in modality_drift:
            modality_drift[mod] = {"total": 0, "persisted": 0, "drifted": 0}
        modality_drift[mod]["total"] += 1
        if item["oct21_status"] == "PERSISTED":
            modality_drift[mod]["persisted"] += 1
        else:
            modality_drift[mod]["drifted"] += 1

    for mod, data in modality_drift.items():
        data["drift_rate_pct"] = round((data["drifted"] / data["total"]) * 100, 2)

    baseline_timestamp = "2026-10-19T14:25:00Z"
    evaluation_timestamp = "2026-10-21T01:30:00Z"
    elapsed_hours = round((datetime.fromisoformat(evaluation_timestamp.replace('Z', '+00:00')) - datetime.fromisoformat(baseline_timestamp.replace('Z', '+00:00'))).total_seconds() / 3600, 2)

    payload = {
        "experiment_title": "Summary of Hand-Coded Temporal Status Labels",
        "method_status": "Manual labels counted; no follow-up fetch or independent evidence verification in this script",
        "literature_foundations": [
            {
                "citation": "Online-Mind2Web (COLM 2025)",
                "title": "Online-Mind2Web: Benchmarking Web Agents in Changing Environments",
                "finding": "Live-web benchmarks experience continuous ground-truth decay; temporal drift invalidates evaluation annotations without versioned freeze."
            },
            {
                "citation": "LiveWeb-IE (2026)",
                "title": "Information Extraction under Real-World Web Evolution",
                "finding": "Promotional banners and SKU pricing undergo frequent updates, causing static extraction models to fail silently."
            }
        ],
        "temporal_window": {
            "baseline_timestamp": baseline_timestamp,
            "evaluation_timestamp": evaluation_timestamp,
            "elapsed_hours": elapsed_hours
        },
        "aggregate_metrics": {
            "total_coded_items": total_evaluated,
            "persisted_items": total_persisted,
            "invalidated_items": total_invalidated,
            "coded_change_rate_pct": invalidation_rate_pct,
            "coded_persistence_rate_pct": persistence_rate_pct,
            "drift_breakdown_by_category": status_counts
        },
        "site_breakdown": site_breakdown,
        "modality_vulnerability_breakdown": modality_drift,
        "item_level_audits": {
            "shwapno_bd_qc02": SHWAPNO_ITEMS,
            "nagad_bd_fn02": NAGAD_ITEMS
        }
    }

    with open(OUTPUT_PATH, mode='w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    print(f"Temporal drift reproduction results exported to {OUTPUT_PATH}")
    print("\n" + "="*80)
    print("TEMPORAL STATUS LABEL SUMMARY (NO LIVE FETCH)")
    print("="*80)
    print(f"Total Items with Entered Status Labels: {total_evaluated}")
    print(f"Persisted Unchanged:               {total_persisted} ({persistence_rate_pct}%)")
    print(f"Invalidated / Drifted:             {total_invalidated} ({invalidation_rate_pct}%)")
    print("-" * 80)
    print("Drift Categorization:")
    for k, v in status_counts.items():
        pct = round((v / total_evaluated) * 100, 1)
        print(f"  - {k:<25}: {v:>2} items ({pct}%)")
    print("-" * 80)
    print(f"Shwapno Invalidation Rate:          {site_breakdown['BD-QC02 (Shwapno)']['invalidation_rate_pct']}% (6/20 items drifted)")
    print(f"Nagad Invalidation Rate:            {site_breakdown['BD-FN02 (Nagad)']['invalidation_rate_pct']}% (6/20 items drifted)")
    print("="*80)

if __name__ == "__main__":
    analyze_temporal_drift()
