import csv
from collections import defaultdict, Counter

csv_file = "results/information-gap-results-template.csv"

with open(csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total Rows: {len(rows)}")

# Count unique items
items = set(r["item_id"] for r in rows)
print(f"Total Unique Items: {len(items)}")

# Count by page_slot / platform
by_site = Counter(r["page_slot"] for r in rows)
print("\nRows by Site/Slot:")
for site, cnt in sorted(by_site.items()):
    print(f"  {site}: {cnt} rows")

# Count by agent_setup
by_setup = Counter(r["agent_setup"] for r in rows)
print("\nRows by Agent Setup:")
for setup, cnt in sorted(by_setup.items()):
    print(f"  {setup}: {cnt} rows")

# Performance (PASS vs non-PASS) by agent_setup
print("\nOutcomes by Agent Setup:")
setup_outcomes = defaultdict(Counter)
for r in rows:
    outcome = "PASS" if "PASS" in r["agent_reported"] or "Reported correctly" in r["agent_reported"] else "FAIL/BLOCKED"
    setup_outcomes[r["agent_setup"]][outcome] += 1

for setup, outcomes in sorted(setup_outcomes.items()):
    total = sum(outcomes.values())
    p_cnt = outcomes.get("PASS", 0)
    print(f"  {setup}: {p_cnt}/{total} PASS ({p_cnt/total*100:.1f}%)")

# Gaps by modality
print("\nGap Classifications by Modality Surface:")
modality_gaps = defaultdict(Counter)
for r in rows:
    gap = r["gap_classification"]
    modality = r["modality_surface"]
    if gap and gap.lower() != "none":
        modality_gaps[modality][gap] += 1

for mod, gaps in sorted(modality_gaps.items()):
    print(f"  Modality: {mod}")
    for gap, cnt in gaps.most_common(5):
        print(f"    - {gap}: {cnt}")
