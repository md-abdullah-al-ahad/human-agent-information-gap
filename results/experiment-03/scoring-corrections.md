# Stage-4 scoring correction ledger

**Status (2026-10-21):** Review of existing artifacts only. No new agent runs or webpage captures were made. The master CSV is retained as a historical coded source; the cases below override its `PASS` interpretation where specified. Aggregate Stage-4 accuracy is withdrawn until a common rubric is applied to every item and the Chaldal prose rows.

| Item / arm | Historical label | Conflict visible in saved case report | Current interpretation |
|---|---|---|---|
| US-Bangla BD-TR03-04, Qwen with Playwright | PASS | Answer `USBAT15`; reference `USBA15` | Wrong exact promo code. Fail if the code must work exactly. |
| US-Bangla BD-TR03-05, Qwen with Playwright | PASS | Answer `USBAINT10`; reference `USBAIN10` | Wrong exact promo code. Fail if the code must work exactly. |
| 10 Minute School BD-ED01-17, Qwen with Playwright | PASS | Answer `454,545+`; documented reference values `458,543+` / `500,000+` | Disputed; no documented value matches the answer. Capture-time variation requires evidence. |
| 10 Minute School BD-ED01-19, Qwen with Playwright | PASS | Answer `Purnoma Lakshmi`; reference `পূর্ণিমা লস্কর` / Purnima Laskar | Disputed named entity; do not count as exact match. |
| Bangladesh National Portal BD-GV01-07, Qwen with Playwright | PASS | OCR `হেঁকে`; reference `ছেঁকে` | Partial or fail under exact-text criterion; rubric needed. |
| Bangladesh National Portal BD-GV01-08, Qwen with Playwright | PASS | OCR `ডিবিয় তহবিল`; reference `ভবিষ্য তহবিল` | Wrong key term; fail under key-term criterion. |
| Nagad BD-FN02-06, both Gemini arms | PASS | One answer identifies Tariq Kazi and the other Jamal Bhuyan; reference lists both names | Ground truth ambiguous. Suspend both passes until independent image review. |
| Chaldal BD2-20, Gemini with Playwright and both static arms | Gap `None`; no coded score | Agents say Fresh from an asset filename; case report says graphic is MGI | Partial under existing case report; do not count as full success. |

The [source review manifest](source-reviewed-corrections.json) now records exact artifact hashes and row-specific dispositions for all 11 flagged agent-item rows. Seven have direct saved-pixel support: the two US-Bangla codes, the parent name, the oil-advisory wording, and the three Chaldal logo-list answers. The 10 Minute School download count remains unresolved because the saved DOM says `৫,০০,০০০+` while the older inventory says `৪,৫৮,৫৪৩+` and historical timing is not aligned. The government GPF carousel frame is not in the retained screenshot, so its key-term correction remains provisional. The two Nagad person identities remain unverified by the unlabeled saved image. These are **source reviews of selected disputes**, not a complete rescore.

The [master CSV](../information-gap-results-template.csv) also has 22 Chaldal rows per arm with descriptive `agent_reported` text instead of score codes. This makes a naive `PASS`-prefix count understate those arms by 22 rows each. The [cross-site synthesis](cross-site-benchmark-synthesis-report.md) therefore reports label counts, not an accuracy table. The [worklist](../item-adjudication-worklist.csv) carries the source-reviewed outcomes in separate fields while retaining every historical answer and label. Do not recompute aggregate accuracy until the remaining rows have the same source and rubric review.
