# Website information audit protocol (Stage 1)

**Status:** exploratory protocol, version 0.2 (2026-10-18). This document defines observation, not expected findings. Pilot 01 is exploratory and its tool-assisted observations are provisional until human review.

## 1. Unit of comparison and scope

The unit is one **question about one page and selected-variant state**, observed at a recorded time. Compare (a) what a human can substantiate from the rendered page, (b) what an AI system can access and retrieve from that same state, and (c) what it concludes when given the same frozen evidence. The human reference describes **what the website states or displays**, not whether the product works as advertised. Do not turn a seller claim into independently verified product truth. Price and availability are time- and location-dependent observations, not durable product facts.

Record both the question's scope (`page_says`, `page_displays`, or `external_fact`) and the inspected surface (for example, title, price block, purchase controls, specifications, description, images, variant selector, reviews). Mark whether a statement was seen in the rendered interface, text extraction, page metadata, or an image; these are different evidence surfaces. An `external_fact` may remain unknown from the page. Search results and other pages are outside the reference unless explicitly included in the question.

## 2. Sampling websites and pages

For the pilot, use one public Bangladeshi site, [Daraz Bangladesh](https://www.daraz.com.bd/). The name and domain identify the sampling frame; they are not evidence about any product. Later audits should vary website type, domain, language, and interaction pattern through declared strata, not by selecting only failures.

Before opening product content for annotation, record the site, date, locale, location, browser/device, login state, search query, sort order, and inclusion rules. Choose three distinct public product URLs with a reproducible rule, then freeze those URLs and page/variant IDs before asking the evaluation questions. Retain rejected candidates and reasons in selection notes. Avoid pages requiring purchase, login, or personal data. A missing candidate is a sampling outcome, never proof that the product or feature is unavailable.

### Minimal pilot page slots

| Slot | Selection rule at pilot start |
| --- | --- |
| P1 | Search `iPad paperlike screen protector`; take the first eligible product page in the site's default order that is visibly marketed as paperlike or equivalent in its listing title. If none among the first 20 results, record that limit and take the first eligible iPad screen protector instead. |
| P2 | Search `iPad screen protector`; take the first eligible distinct product page, regardless of its claims. |
| P3 | Search `iPad case`; take the first eligible distinct product page to check whether the method works outside screen protectors. |

Eligibility means a reachable, individual product page with a stable URL or product ID and content a logged-out human can inspect. Record the selected URL, final URL, variant, search result position, and selection time. If a slot cannot be filled, mark it **unfilled** with the observed reason and report fewer than three pages; do not silently replace the site or broaden the rule. Product URLs are intentionally unfilled now because live listings may change before collection.

## 3. Human reference and evidence capture

Use a logged-out browser session with recorded locale and location. On each frozen URL, note the initial and final URL, load status, time in UTC, and any consent, region, or variant state. Inspect visible title, current price and currency, purchase controls and any explicit stock message, options, specifications, description, images with readable text, and relevant expandable sections. Record exactly which sections were checked. Click at most one alternate variant per page in the pilot, without adding to cart or purchasing; record the selected option, URL, price, and purchase-control state before and after. Save timestamped screenshots of the relevant rendered view and short verbatim excerpts or transcriptions linked to page regions. If content changes during the session, save both states and mark the question unstable. An enabled purchase button is not by itself proof of stock.

For every question, the first **human** reviewer records an answer, an evidence state, and a pointer to supporting or contradicting evidence. A second reviewer independently checks the three pages' question answers where possible, blinded to AI output. Resolve disagreements by revisiting the frozen capture; retain both initial judgments and the resolution. If one human reviewer is available, label the reference **provisional**. Tool-assisted observations made by the investigating AI are **not** human references; store them separately and leave human reference and formal scores blank until review. Do not force consensus where evidence is ambiguous.

Use these reference states:

| State | Meaning |
| --- | --- |
| `supported_true` | The bounded proposition is explicitly supported by visible page evidence. |
| `supported_false` | The bounded proposition is explicitly contradicted. For a claim about whether wording appears, it can also mean absence after a complete, recorded inspection of the defined scope. |
| `not_stated` | The inspected page scope is accessible and complete enough to establish that no relevant statement was found. This says nothing about the product's actual properties, stock, or other pages. |
| `ambiguous` | The page is conflicting, unclear, variant dependent, or insufficient to decide. |
| `human_inaccessible` | The human could not inspect the required page scope under the recorded conditions. |
| `not_checked` | Inspection was not completed. |

Keep `not_stated` separate from `human_inaccessible`, `ambiguous`, and `supported_false`. A false product claim needs contradictory evidence, not merely missing text. For a negative product claim such as “incompatible with model X,” require an explicit statement or an independently justified closed scope. Absence of a compatibility claim never establishes incompatibility. An AI access error likewise never establishes absence of content. If only a tool's partial extraction lacks a field, label that field **not retrieved by that method**, not **not stated on the page**.

For exploratory AI observations before human review, use `observed_support`, `observed_contradiction`, `not_observed_in_inspected_scope`, `ambiguous`, `method_inaccessible`, or `not_checked`. These describe the investigator's evidence only; they are not truth labels. A grouped page record may share page metadata across its nine question observations. Formal scoring still uses one page-question-state row in the results CSV.

## 4. AI runs: retrieval and interpretation

Freeze the human capture before **formal** AI scoring. Use the same question text for each page; record the exact prompt, model and version, OpenRouter provider if exposed, reasoning configuration if exposed, interface, enabled tools, locale, run time, URL(s) attempted, redirects, response, citations, and errors. Write `not exposed` for unknown runtime metadata rather than guessing. Keep raw outputs and tool traces. Do not edit prompts after seeing a failure within a run; any retry is a new, labeled run. One primary run per page/question is sufficient for a later formal evaluation; optional repeats must be declared and counted separately.

1. **Live-page run:** Give the AI the frozen product URL and question. Ask it to report the answer or abstain, its evidence location, and whether it accessed the page. Score **retrieval** first: did its trace contain the specific human-visible evidence needed for the answer, with a valid page/location reference? Record `retrieved`, `partial`, `not_retrieved`, `access_failed`, or `unobservable_trace`. A fluent answer is not evidence that retrieval succeeded.
2. **Evidence-only run:** Give the AI a frozen evidence bundle from the human capture (relevant excerpts and image descriptions/transcriptions, with locations), without the human answer or grade. Ask the same question. Score **interpretation** only against what this bundle supports. This controls for retrieval differences, although the bundle itself may omit context; record its exact contents and ID.
3. **End-to-end comparison:** Compare the live answer to the human reference. If live retrieval missed evidence but the evidence-only answer is correct, classify a retrieval-stage symptom. If the correct evidence was retrieved but the answer is wrong, classify an interpretation-stage symptom. If traces are insufficient, mark stage undetermined.

Use the same instructions for all three pages, including an explicit option to answer `unknown` or `cannot access`. Do not reveal reference labels to the AI. Match URL, selected variant, locale/location, observation window, and available page scope as closely as practical. If one method receives a rendered screenshot and another receives text only, report them as different retrieval conditions, not a fair head-to-head model comparison. Where a tool cannot expose a trace, do not infer which stage failed. The investigator's own responses in Pilot 01 are exploratory observations, not independent model scores.

Fixed instruction for both runs, followed by the exact question: “Answer using only the supplied product page or evidence bundle. State what the page says, cite the relevant page section or evidence item, and distinguish a listing claim from independently verified fact. For price and availability, report the selected variant, currency, and observation time. If evidence is missing, say `unknown` or `not stated` as appropriate. If you cannot access the required content, say `cannot access`. Do not infer that a product, feature, or stock is unavailable from missing content or an inactive control.” Supply only the URL in the live run; supply only the frozen evidence bundle in the evidence-only run. Save the full assembled prompt, including any platform instructions, for each run.

## 5. Claims, uncertainty, and scoring

For each response, split compound answers into atomic claims. A **supported positive** needs a matching cited passage or visible element in the frozen page state. A **supported negative** needs an explicit negation or a complete, bounded inspection for a question about *what the page says*. Mark unsupported additions even when the main answer is correct. Check cited locations against the capture; a plausible but mismatched citation is unsupported.

Record the response decision as `answer`, `qualified_answer`, `abstain_unknown`, or `abstain_access`. Judge whether that decision is appropriate given the reference state and the system's actual access. `ambiguous`, `human_inaccessible`, and external facts unsupported by the page generally warrant a qualified answer or abstention. An AI that says “not available” after failing to load a page is making an unsupported negative claim. Human inaccessibility makes the case unscorable for content accuracy, but access behavior and uncertainty remain observable.

Failure codes describe **observed symptoms**, not mechanisms: `access_failure`, `retrieval_omission`, `wrong_variant_or_state`, `misinterpretation`, `unsupported_inference`, `false_absence`, `citation_mismatch`, `overconfidence`, `unwarranted_abstention`, `conflict_mishandling`, `other`, or `undetermined`. Assign multiple codes if needed. Put any proposed cause (JavaScript rendering, locale, tool limits, etc.) in a separate **hypothesis** field with supporting evidence and confidence; default to `unknown`. Investigate causes only after the observation is recorded.

## 6. Pilot questions and observations

Ask these nine questions on each selected page (27 planned page-question records). Q1–Q5 are unchanged from v0.1; Q6–Q9 add the commercial and interactive page state. Answers may be `not stated`, `unknown`, or `cannot access` where warranted:

| ID | Exact question | Main check |
| --- | --- | --- |
| Q1 | What product title and product type are displayed on this page? | Basic positive extraction. |
| Q2 | Which iPad models, if any, does this page explicitly list as compatible? | Extract exact model names without inferring others. |
| Q3 | Does this page explicitly describe the product surface as paperlike, paper-like, matte, or textured? Quote the wording if present; otherwise say whether it is not stated in the inspected page scope. | Bounded presence/absence; no inference about actual texture. |
| Q4 | Does this page explicitly state that the product is incompatible with any iPad model? Quote the model and wording if present; otherwise say whether it is not stated in the inspected page scope. | Negative claim and false-absence control. |
| Q5 | What, if anything, does this page claim about Apple Pencil use, and what can be verified about real-world performance from this page alone? | Separate seller claim, uncertainty, and verification. |
| Q6 | What price and currency are displayed for the selected variant at the observation time? | Time-bound price extraction. |
| Q7 | What does the page explicitly state about availability, and what purchase controls are enabled or disabled? | Separate explicit stock text from interface state. |
| Q8 | What product specifications are explicitly displayed in dedicated specification or detail fields? Give field/value pairs and their source section. | Bounded specification extraction, including contradictions. |
| Q9 | Which variant groups and selected values are visible? After selecting one alternate option, what changes in price, URL, compatibility wording, and purchase-control state? | Interactive variant state; `cannot assess` if controls are inaccessible. |

Use the same wording for human annotation and AI runs. Record page-specific inapplicability (for example, an iPad case with no surface claim) rather than changing the question. A **successful observation** has a frozen page state, complete metadata, human evidence state with location, raw AI outputs/traces, and an adjudicated or explicitly unscorable comparison. A **failed observation** is an incomplete attempt (missing page, capture, trace, or metadata); retain it with a reason. A correct AI answer and an AI error are both valid observations if adequately evidenced. Do not discard ambiguous or failed cases to improve scores.

## 7. Records, metrics, and validity

Copy `data/pilot-observation-template.json` once per page-question-state record; shared page evidence may be referenced from multiple records. Use `results/pilot-results-template.csv` for one **formally adjudicated** row per record; leave it empty for provisional exploratory observations. Templates contain no observations. Store timestamps in UTC, preserve original language and currency, and record any translation separately. Record URL plus final URL, product/variant ID, content state, reviewer IDs, browser/device/version, model/version, provider/reasoning configuration if exposed, tool configuration, prompt, attempts, and evidence file paths; hash captures when practical. Do not silently correct original records; append a dated correction that points to the original. Remove personal data from screenshots and logs. Review captures for rights and privacy before committing them.

For the results sheet, use `complete`, `incomplete`, or `unscorable` for `record_status`; `correct`, `partial`, `incorrect`, or `unscorable` for interpretation and end-to-end grades; and `yes`, `no`, or `not_applicable` for citation and abstention judgments. Count unsupported and false-absence atomic claims as nonnegative integers. Keep retrieval grades as defined in Section 4. Put multiple failure symptoms in a semicolon-separated cell. A `not_stated` answer can be correct for Q3 or Q4 only if the inspected page scope was complete enough to justify it; it is never evidence that the physical feature is absent.

Report **counts with denominators** for this small pilot, not just percentages: pages human-accessible; question records with adjudicable references; required evidence retrieved in live runs; correct interpretation given frozen evidence; correct end-to-end answers; unsupported atomic claims; false-absence claims; appropriate abstentions on unknown/inaccessible cases; citation matches; and variant-state changes retrieved. Separately report partial, ambiguous, and unscorable cases. Use a simple table by page and question before any aggregate. Do not calculate accuracy against provisional AI observations. No significance testing or generalization from 27 records.

Main validity threats and controls:

- **Dynamic listings, variants, region, and personalization:** collect near-contemporaneous human and AI runs; freeze URLs, variants, locale, and screenshots; mark drift instead of adjudicating across different states.
- **Reference error or incomplete inspection:** record the inspected scope and evidence; seek a blinded second check; retain unresolved cases.
- **Prompt or tool asymmetry:** preserve exact prompts and tool access; interpret the live and evidence-only runs as different conditions, not directly interchangeable scores.
- **Unobservable AI retrieval:** score `unobservable_trace` and avoid causal attribution.
- **Selection bias and tiny sample:** apply the declared first-eligible rule, retain exclusions and substitutions, and report case-level findings without population claims.
- **Ambiguous language and seller assertions:** keep original wording, distinguish page claims from real-world facts, and allow unresolved judgments.
- **Researcher hindsight:** freeze questions and labels before inspecting AI responses; log any protocol change and do not silently rescore old runs.

After the pilot, review where the protocol was hard to apply, revise definitions with dated reasons, and only then decide on broader sampling or experiments. Do not treat early failure patterns as established causes or solutions.

## Version history

- **v0.1:** Initial sampling, human reference, retrieval/interpretation split, claim states, and five pilot questions.
- **v0.2 (2026-10-18):** Added time- and variant-specific price/availability/specification checks (Q6–Q9); distinguished rendered content from text extraction, explicit stock from enabled controls, and missing evidence from method inaccessibility; added fair-comparison conditions and runtime metadata; separated exploratory AI observation from human reference and formal scoring; required append-only corrections.
