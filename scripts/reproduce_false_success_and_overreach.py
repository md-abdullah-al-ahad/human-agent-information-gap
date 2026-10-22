#!/usr/bin/env python3
"""Describe existing benchmark labels without inventing claim-level accuracy.

The master CSV mixes pass codes with prose, and its rows are information items,
not atomic final-answer claims. This script reports only reproducible counts of
those existing labels and explicit pilot examples. It makes no live requests.
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "results/information-gap-results-template.csv"
OUTPUT_PATH = ROOT / "results/reproduced-false-success-overreach-results.json"

STOCK_IDS = {"P1-06", "P1-07", "P2-05", "P2-06", "P3-04", "P3-05"}
NEGATIVE_IDS = {"P2-12", "P3-13"}


def outcome_label(value: str) -> str:
    value = value.strip().upper()
    if value.startswith("PASS"):
        return "PASS_PREFIX"
    if value.startswith("FAIL"):
        return "FAIL_PREFIX"
    if value.startswith("PARTIAL"):
        return "PARTIAL_PREFIX"
    return "DESCRIPTIVE_UNSCORED"


def main() -> None:
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    by_setup = defaultdict(list)
    for row in rows:
        by_setup[row["agent_setup"]].append(row)

    setup_counts = {}
    for setup, subset in sorted(by_setup.items()):
        labels = Counter(outcome_label(row["agent_reported"]) for row in subset)
        setup_counts[setup] = {
            "item_rows": len(subset),
            "outcome_label_counts": dict(labels),
            "descriptive_rows_by_page": dict(Counter(
                row["page_slot"] for row in subset
                if outcome_label(row["agent_reported"]) == "DESCRIPTIVE_UNSCORED"
            )),
        }

    stock_rows = [row for row in rows if row["item_id"] in STOCK_IDS]
    negative_rows = [row for row in rows if row["item_id"] in NEGATIVE_IDS]
    absent_human_rows = [row for row in rows if not row["human_accessible"].lower().startswith("yes")]

    payload = {
        "analysis_status": "Descriptive recount of legacy CSV labels; not an adjudicated claim-precision study",
        "method_limitations": [
            "Each row is an information item for one agent, not necessarily one atomic factual claim.",
            "The CSV uses prose outcomes for some sites and PASS/FAIL codes for others.",
            "Tool exposure fields refer to different tool scopes and cannot be pooled as a single four-stage recall metric.",
            "Unstated/absent items should not be counted as human-visible positive facts.",
            "No independent claim-to-evidence adjudication is performed by this script.",
        ],
        "dataset_item_rows": len(rows),
        "distinct_item_ids": len({row["item_id"] for row in rows}),
        "rows_with_nonpositive_human_reference": len(absent_human_rows),
        "results_by_setup": setup_counts,
        "pilot_examples": {
            "stock_affordance": {
                "item_ids": sorted(STOCK_IDS),
                "rows": len(stock_rows),
                "note": "Six item IDs duplicate three page-level stock assertions across two agents. The pilot reports six agent answers asserting stock without an explicit stock statement; physical stock is unknown.",
            },
            "absence_to_negation": {
                "item_ids": sorted(NEGATIVE_IDS),
                "rows": len(negative_rows),
                "note": "Four agent-item rows describe categorical incompatibility claims from missing selector options. Physical compatibility is unknown.",
            },
        },
        "known_scoring_conflicts": [
            "BD2-20: three arms report Fresh from an asset filename where the site audit identifies MGI; the CSV gap field says None.",
            "BD-TR03-04/05: exact promo codes differ in one PASS-labeled arm.",
            "BD-ED01-17/19 and BD-GV01-07/08: PASS labels coexist with different numbers, names, or OCR text in site tables.",
        ],
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)

    print(f"Counted {len(rows)} existing agent-item rows across {payload['distinct_item_ids']} IDs.")
    for setup, data in setup_counts.items():
        print(f"{setup}: {data['outcome_label_counts']}")
    print("No claim-level precision or four-stage recall is calculated.")


if __name__ == "__main__":
    main()
