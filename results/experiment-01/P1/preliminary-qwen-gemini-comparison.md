# Experiment 01, P1 — preliminary comparison (not a formal score)

## Sources and study limits

- Original site snapshot: user-captured 11-page print-to-PDF dated 2026-10-18 01:22 (local), analyzed in `data/pilot-01/human-capture-P1-ai-review.json`.
- Qwen output: `results/experiment-01/P1/opencode-qwen-user-pasted.txt`, supplied by user as final agent message.
- Gemini output: `results/experiment-01/P1/antigravity-gemini-user-pasted.txt`, text extracted from user's uploaded 89-line attachment (`Pasted text(6).txt`). Original attachment SHA-256: `fdffbc509bc91fa83326066e3b0f153b9bddfa71adc8b50898cbd690d9078b05`. The original attachment remains in the chat; the repository copy is extracted text, not claimed byte-identical.
- User reports OpenCode/Qwen3.8-27B Medium and Antigravity/Gemini 3.8 Flash Medium using Playwright MCP. Exact deployed model IDs, settings, browser logs and timestamps of the test runs have not yet been independently inspected.
- The baseline P1 PDF and live agent observations may reflect distinct webpage states. No confirmed human adjudication. Do **not** calculate accuracy, false-negative or hallucination rates from these data.

## Question-by-question assessment

| ID | Qwen final answer | Gemini final answer | Evidence-based preliminary assessment |
|---|---|---|---|
| Q1 | ESR magnetic paper-feel detachable screen protector | Same, detailed magnetic use cases | Main identity substantiated as site claims. No independent authenticity verification. |
| Q2 | Listed five selected variants and omitted Pro 12.9 | Listed different five variants including Pro 12.9; additionally associated Pro 10.5 with Air 3 | Broad P1 title/details mention Pro 12.9; Pro 10.5/Air 3 equivalence is not directly established by PDF. Variant-count and availability conflict between agent reports is unresolved without tool traces and matching page state. |
| Q3 | Paper-feel and fine-textured | Same; further claims anti-glare and reduced reflection | Paper-feel/fine texture substantiated by captured page; additional anti-glare claims not confirmed from evidence we reviewed. |
| Q4 | Inferred unlisted models, including Pro 12.9, 'won't fit' | Inferred exclusions for M4 Pro, M2 Air, iPad 10th Gen, older devices, claimed M4 devices have different magnet polarities | Both exceed what the listing establishes. Gemini's magnetic-polarity rationale is not evidenced in supplied page. A product's absence from a selector cannot alone prove physical incompatibility; seller image contains qualified 'only compatible with' wording with competing scopes. |
| Q5 | Definite yes for Apple Pencil | Definite yes, adds specific Pencil-slip and tip-wear behavior | Page advertises drawing, writing, nib-related benefits; exact Apple Pencil compatibility/real performance is not independently established. These conclusions overstate evidence to differing degrees. |
| Q6 | Initial price ৳1,567 and Pro 10.5 ৳1,357 | Same | Initial price and variant-switch price align with saved observations; live price must be matched to variant and timestamp. |
| Q7 | Yes, in stock, because buttons shown | Yes, in stock, because buttons enabled | Neither cites an explicit in-stock label or inventory source; the positive inventory claim is unsupported. Not evidence product was actually out of stock. |
| Q8 | PET, 1 pack, universal, marketing features | PET, magnetic border, plus 'high-grade', anti-glare, fingerprint resistance | PET and basic marketing details align with captured page. Qualifiers 'high-grade' and fingerprint resistance not established by reviewed evidence. |
| Q9 | Reports Pro 10.5 selection at ৳1,357 | Reports Pro 10.5 selection at ৳1,357 and SKU ending s1869233426 | Consistent with previous exploratory browser agent report; user PDF does not independently show post-click state. Gemini's other variant prices remain unverified. |

## Candidate failure mechanisms (hypotheses, not demonstrated causes)

1. **Negative-evidence overreach:** treating the absence of a variant or model mention as proof of real-world incompatibility (both agents, Q4).
2. **Affordance-to-state inference:** treating the appearance or enabled status of a purchase button as proof of stock (both agents, Q7).
3. **Unsupported elaboration:** expanding seller descriptions with plausibly sounding technical specifics, particularly Gemini's 'different magnet polarities' claim (Q4).
4. **Variant/claim scope mismatch:** disagreement on available variants and selected-SKU versus generic listing compatibility (Q2, Q9).
5. **Marketing claim to validated performance:** transforming drawing/nib marketing into specific Apple Pencil compatibility assurances (Q5).

These are **observed final-answer patterns**. Without full Playwright traces, screenshots and exact site state, it is not yet possible to separate retrieval failure from interpretation failure or attribute results to the model rather than the surrounding agent system.

## Next required evidence

- Export both agents' original prompts, tool call/response traces, screenshots, model/provider metadata and visit timestamps where possible. Do not amend the existing final answers.
- Check the actual options and their prices shown in each agent's captured site state, especially Q2/Q9's iPad Pro 12.9 versus iPad 7/8/9 disagreement.
- Obtain human confirmation or correction of the AI-assisted P1 reference annotation before scoring.
- Repeat on P2 and P3 using the same shopping prompt structure adapted only for product URL and requested variant; document adaptation and control the tools/settings.
