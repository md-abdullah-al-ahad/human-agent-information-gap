"""Build a row-level review worklist from saved benchmark labels.

This does not rescore the benchmark. Historical labels remain separate from
adjudicated outcomes, and an empty corrected_outcome means no review occurred.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/information-gap-results-template.csv"
DESTINATION = ROOT / "results/item-adjudication-worklist.csv"
SOURCE_REVIEW = ROOT / "results/experiment-03/source-reviewed-corrections.json"

# These statuses restate the documented correction ledger; they are not fresh
# adjudications and are deliberately excluded from any aggregate score.
KNOWN_ISSUES = {
    "BD-TR03-04": ("wrong_exact_code", "fail_exact_text"),
    "BD-TR03-05": ("wrong_exact_code", "fail_exact_text"),
    "BD-ED01-17": ("reference_time_or_value_dispute", "unresolved"),
    "BD-ED01-19": ("named_entity_dispute", "unresolved"),
    "BD-GV01-07": ("ocr_text_mismatch", "unresolved"),
    "BD-GV01-08": ("wrong_key_term", "fail_key_term"),
    "BD-FN02-06": ("ambiguous_visual_reference", "unresolved"),
    "BD2-20": ("logo_identity_dispute", "partial_in_case_report"),
}

FIELDS = [
    "source_csv_row", "item_id", "page_slot", "agent_setup", "information_category",
    "modality_surface", "human_accessible_reference", "tool_exposed_historical",
    "agent_retrieved_historical", "agent_reported_historical", "gap_classification_historical",
    "evidence_location_historical", "capture_dom", "capture_screenshot", "capture_provenance",
    "review_priority", "review_reason", "review_state", "corrected_outcome",
    "adjudicated_claim", "evidence_locator", "evidence_sha256", "adjudicator_notes",
]


def _source_reviews() -> dict[int, dict[str, str]]:
    """Load separately documented reviews, failing if their saved sources drift."""
    reviews = {}
    for review in json.loads(SOURCE_REVIEW.read_text(encoding="utf-8")):
        row_number = review["source_csv_row"]
        if row_number in reviews:
            raise ValueError(f"duplicate source review for CSV row {row_number}")
        for artifact in review["evidence_artifacts"]:
            path = ROOT / artifact["path"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != artifact["sha256"]:
                raise ValueError(f"source review artifact changed: {path}")
        reviews[row_number] = review
    return reviews


def _capture_map() -> dict[str, tuple[str, str, str]]:
    mapping = {}
    for entry in json.loads((ROOT / "data/stage-3/manifest.json").read_text()):
        mapping[entry["slot"]] = (entry["dom_file"], entry["screenshot_file"], "stage-3 manifest")
    stage4 = json.loads((ROOT / "data/stage-4/manifest.json").read_text())["sites"]
    for slot, entry in stage4.items():
        mapping[slot] = (entry["raw_dom"]["path"], entry["screenshot"]["path"],
                         "stage-4 manifest; site-level timestamp only")
    mapping["BD1"] = mapping["BD-01"]
    mapping["BD2"] = mapping["BD-02"]
    for slot in ("P1", "P2", "P3"):
        mapping[slot] = ("", f"data/pilot-01/screenshots/{slot}-initial.png",
                         "pilot screenshot; referenced human PDF absent")
    return mapping


def build_rows() -> list[dict[str, str]]:
    captures = _capture_map()
    reviews = _source_reviews()
    output = []
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            slot = row["page_slot"]
            capture = captures.get(slot, ("", "", "capture mapping missing"))
            item_id = row["item_id"]
            reported = row["agent_reported"]
            known = KNOWN_ISSUES.get(item_id)
            review = reviews.get(row_number)
            if review and (review["item_id"] != item_id or
                           review["expected_agent_reported"] != reported or
                           review["expected_agent_setup"] != row["agent_setup"]):
                raise ValueError(f"source review no longer matches CSV row {row_number}")
            correction_applies = False
            if known:
                if item_id in {"BD-TR03-04", "BD-TR03-05", "BD-ED01-17", "BD-ED01-19",
                               "BD-GV01-07", "BD-GV01-08"}:
                    correction_applies = "OpenCode" in row["agent_setup"] and "With Playwright" in row["agent_setup"]
                elif item_id == "BD-FN02-06":
                    correction_applies = "Antigravity" in row["agent_setup"]
                elif item_id == "BD2-20":
                    correction_applies = "Fresh" in reported
            reasons = []
            if item_id == "BD2-20" or slot == "BD2":
                reasons.append("Chaldal uncoded prose row")
            if correction_applies:
                reasons.append(known[0])
            if slot.startswith("P") and len(slot) == 2:
                reasons.append("original pilot human PDF absent")
            if not row["human_accessible"].strip().lower().startswith("yes"):
                reasons.append("human reference is not a positive visible fact")
            output.append({
                "source_csv_row": str(row_number), "item_id": item_id, "page_slot": slot,
                "agent_setup": row["agent_setup"],
                "information_category": row["information_category"],
                "modality_surface": row["modality_surface"],
                "human_accessible_reference": row["human_accessible"],
                "tool_exposed_historical": row["tool_exposed"],
                "agent_retrieved_historical": row["agent_retrieved"],
                "agent_reported_historical": reported,
                "gap_classification_historical": row["gap_classification"],
                "evidence_location_historical": row["evidence_location"],
                "capture_dom": capture[0], "capture_screenshot": capture[1],
                "capture_provenance": capture[2],
                "review_priority": "high" if reasons else "normal",
                "review_reason": "; ".join(reasons),
                "review_state": (review["review_state"] if review else
                                 "documented_correction_pending_evidence_review" if correction_applies else "pending"),
                "corrected_outcome": (review["corrected_outcome"] if review else
                                      known[1] if correction_applies else ""),
                "adjudicated_claim": review["adjudicated_claim"] if review else "",
                "evidence_locator": review["evidence_locator"] if review else "",
                "evidence_sha256": ("; ".join(artifact["sha256"] for artifact in review["evidence_artifacts"])
                                    if review else ""),
                "adjudicator_notes": review["adjudicator_notes"] if review else "",
            })
    unknown_rows = set(reviews) - {int(row["source_csv_row"]) for row in output}
    if unknown_rows:
        raise ValueError(f"source reviews refer to missing CSV rows: {sorted(unknown_rows)}")
    return output


def main() -> None:
    rows = build_rows()
    with DESTINATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} historical agent-item rows to {DESTINATION}")
    print(f"Source-verified disputed rows: {sum(row['review_state'] == 'source_verified' for row in rows)}")
    print(f"Source-checked but unresolved disputed rows: "
          f"{sum(row['review_state'] == 'source_checked_unresolved' for row in rows)}")


if __name__ == "__main__":
    main()
