# Experiment 01 — Cross-case synthesis of three-page naturalistic shopping pilot

**Date:** 2026-10-18. **Status:** preliminary, exploratory, hypothesis-generating. No generalizable error-rate estimates, no calibrated confidence results, no independently confirmed gold standard.

## Design and denominators

Three Daraz product pages: P1 magnetic paper-feel removable screen protector; P2 two-piece glass screen protector with ambiguous 'case/cover' naming; P3 foldable iPad case. Two agent setups: OpenCode/Qwen3.8-27B through OpenRouter and Antigravity/Gemini 3.8 Flash, each Medium; Playwright MCP available to both.

**Six final-answer runs** (three pages × two agents × one run). All six were given product-specific **naturalistic shopping prompts** based on nine question families, but wording adapted for P3 (a case rather than protector). Tool outputs, variant selection behavior, and final responses were inspected. Data are not independently sampled websites or multiple random-seed repetitions. Raw session traces can contain local private information and are held outside the repository. Page content was captured earlier than agents browsed; dynamic claims require variant and timestamp-specific evidence.

## Cross-case patterns observed

| Pattern | P1 | P2 | P3 | What this shows—and does not show |
|---|---|---|---|---|
| Both assert 'in stock' from buttons/no sold-out wording | Yes | Yes | Yes | In **all six pilot answers**, stock confidence exceeds explicit stock evidence preserved in our audits. This is an evidence-support observation, **not six proven factually false stock statuses**. |
| Both infer categorical physical incompatibility from missing variants/selection options | Yes | Yes | Yes | Recurrent **negative-evidence overreach**, though different pages have distinct seller image statements and some technical compatibility may in fact be false/true independently of seller claims. |
| Both recover requested alternate variant price | Yes, Pro 10.5 ৳1,357 | Yes, A16 ৳856 | Yes, Air case ৳1,217 | Pricing interaction is an observed **success pattern**, not a claim of general browser reliability. |
| Visually inspect seller marketing images using image tool | Neither confirmed | Both attempted | Both attempted | Changes in strategy coincide with changes of page and task: **cannot attribute to experience or causal improvement**. The transcripts do not embed the image pixels. |
| Question-specific unsupported/contradictory elaboration | Gemini adds magnetic-polarity account; Qwen mislists selectable variants | Qwen says A16 price cheapest though Mini 6 cheaper; categorical package-content exclusions | Gemini asserts Pencil storage/charging details not established by reference; Qwen says not evidenced | Both positive and negative unsupported claims, and internal consistency failures, are candidate outcomes to score in a larger blinded test. |
| Appropriate contextual disambiguation | Variation vs general title partly missed | Glass protector identity broadly retrieved despite ambiguous 'case' title | Both distinguish temporary case transit film from separate screen protector | Successful reasoning is also present, so avoid failure-only sampling/analysis. |

## What these observations cannot establish

1. A model-only performance ranking. Agents have different scaffolds, runtime histories, browser action selection, file/shell tools, session state, and page times.
2. Accurate rates: three intentionally small same-domain pages and six one-off runs are insufficient for uncertainty intervals, calibration, or population inference.
3. Retrieval-vs-reasoning causal attribution except for narrow cases where exact tool output and final answer show a discrepancy, e.g., missing stock label alongside confident stock claim; even there, no validated inventory fact exists.
4. Negative truth: inability to find a model name or an explicit stock label does not prove genuine incompatibility or genuine unavailability.
5. Fidelity of vision: records contain image-view events, but the original image bytes were not embedded in export. The static human-facing PDF is interpreted provisionally by AI and requires human review.
6. Vendor-seller marketing accuracy, physical fit, Apple Pencil performance, or shipment contents.

## Candidate targeted follow-ups

**A. Separate extraction from inference.** For a preselected set of new site/question pairs, capture browser-visible evidence, then test (i) free browsing under naturalistic shopping prompts and (ii) each model answering from exactly the same frozen evidence bundle. Use a held-out set of pages and do not leak reference labels or error taxonomy in the agent prompts. This helps distinguish access-related omissions from conclusions drawn on equal inputs.

**B. Vary strength of negative evidence.** Construct or carefully sample cases with (1) explicit negative statements, (2) complete bounded lists, (3) incomplete positive mentions, (4) silence, and (5) conflicting image/text claims. Pre-annotate the observable source statements and the question's scope. Score factual support, negative overreach, justified abstention, and confidence *after* independent adjudication.

**C. Study multimodal access.** Compare text/DOM-only against text+verified image-pixel access on the same page state. Many of our pilot attributes were embedded in seller promotional images.

**D. Broaden domain coverage.** The research concerns the human–agent information gap on **websites in general**. Add service, policy, institutional, documentation, accessibility, or booking information pages with precise, legal, reproducible reference capture, rather than oversampling Daraz product listings.

## Immediate handoff

- [P1 trace audit](P1/tool-trace-audit.md)
- [P2 paired trace audit](P2/paired-qwen-gemini-trace-analysis.md)
- [P3 paired trace audit](P3/paired-qwen-gemini-trace-analysis.md)

Before any paper-level claim: (a) independent human adjudication of pilot observations, especially P3 Pencil slot; (b) lock codebook and candidate hypotheses; (c) preregister or prospectively freeze the next sample and evaluation criteria; (d) avoid feeding findings to evaluated agents.
