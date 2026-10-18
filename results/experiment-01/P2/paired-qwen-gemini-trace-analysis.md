# Experiment 01 — P2 matched shopping task: paired agent and tool-trace review

**Review status:** exploratory, qualitative, **not** a formal score or independently human-verified ground truth. Reviewed 2026-10-18.

## Input provenance

- P2 product: `https://www.daraz.com.bd/products/-i567669430.html`.
- Both original user prompts ask the same nine natural-language shopping questions and request the `For iPad A16 2025` option.
- **Correct Qwen/OpenCode session:** user-uploaded `p2real-qwen.json`, SHA-256 `48968cc962dc19219ed07ae69f9818af90b05fd7a0568a9cfe26c878dff6888b`, session `ses_eb1c8c316ffe1B4eNz4zjbvuLR`; OpenCode 1.19.3, OpenRouter `qwen/qwen3.8-27b`, `medium`. Original final answer is archived without editing at [Qwen response](opencode-qwen-user-exported-answer.md).
- **Gemini/Antigravity session:** user-uploaded `p2-gemini.json` (and its JSONL serialization), SHA-256 `d477dace04f39d5a6b7b0168bf8aeeda74d0264a090db67383ae994081ff561e`, session `3745efbd-e86a-464b-a8e6-9823779e820e`; session model label `Gemini 3.8 Flash (Medium)`. Final answer archived at [Gemini response](antigravity-gemini-user-exported-answer.md); previous [Gemini-only trace audit](gemini-trace-audit.md) predates the corrected Qwen export.
- Human-facing evidence: 6-page user-captured P2 PDF dated 2026-10-18 01:29 local, plus [AI-assisted P2 review](../../../../data/pilot-01/human-capture-P2-ai-review.json). That PDF is in the original ChatGPT conversation, not this repository. Its page state predates the live agent sessions.
- The mistakenly uploaded `p2-qwen.json` is the earlier P1 session and **must not** count toward this P2 experiment.
- Neither raw agent JSON export is committed here: they contain local files, extensive tool payloads and potentially sensitive metadata.

## Browser capabilities and observed workflow

| Observation | Qwen / OpenCode | Gemini / Antigravity |
|---|---|---|
| Shopping prompt | Correct P2 prompt | Correct P2 prompt |
| Timing (UTC) | approximately 08:53:25–08:56:25 | started 08:53:04; completed shopping task later |
| Playwright MCP calls | **27** (3 navigate; 18 evaluate; 2 tabs; 2 snapshot including one error; 1 find; 1 click) | **11** (1 navigate; 9 evaluate; 1 close) |
| Additional agent work | Read DOM snapshot; bash/curl downloaded images; **11** image-read tool calls; inspected `window.__moduleData__` SKU/price structures | Read DOM snapshot; expanded View More; shell downloaded images; **9** image-view tool calls; tested each variant via browser DOM interactions |
| Gallery/description imagery | Downloaded and attempted image inspection | Downloaded and attempted image inspection |
| Can an external reviewer see exact image pixels in the JSON alone? | **No**: read operations indicate image was opened but raw image pixels not embedded in the JSON export | **No**: image-view steps logged but pixels not embedded in JSON export |
| Variant coverage | Extracted 11 SKU/property/price associations from site data, then clicked the specified A16 option | Clicked through 11 options and recorded labels and prices, then chose A16 |
| Tool errors | One targeted Playwright snapshot error; recovered | No confirmed analogous browser failure during shopping task |
| Recorded inference cost | **$0.11817668** (session aggregate); input 77,112, output 6,637, reasoning 5,658, cache read 1,452,416 per OpenCode export | Comparable billed cost not established from Antigravity export |

**Interpretation:** Tools were comparable in *availability* but were not standardized in *use*. Both agents used shell/file/image tooling in addition to Playwright MCP. This is a naturalistic comparison of full agent setups, not a controlled comparison of the underlying model weights or solely MCP execution.

## Variant and price evidence (both agree)

Initial page state: `Color: Pro 11 M4`, `Keyboard language: 2PCS`, **৳872**, strike-through ৳2,266.

Both identified these 11 options with matching observed prices:

| Option | Price |
|---|---:|
| For iPad A16 2025 | ৳856 |
| For iPad 10th | ৳872 |
| Pro 11 2018-2022 | ৳866 |
| 5th 6th 2017 2018 | ৳852 |
| 7th 8th 9th | ৳879 |
| Air 11 M2 | ৳876 |
| Air 4 5 | ৳879 |
| Mini 6 2021 | **৳787** |
| Pro 11 M4 | ৳872 |
| Air 1 2 Pro 9.7 | ৳858 |
| Air 3 Pro 10.5 | ৳877 |

Both successfully selected **For iPad A16 2025**: **৳856**, original ৳2,224, and URL/SKU suffix **`s2608606596`**. This agreement is supported by the individual browser traces and aligns with the older exploratory pilot's A16 price. It does **not** establish current availability outside these captured page states.

**Independent, traceable Qwen error:** Its final answer calls the ৳856 A16 option **"the cheapest variant in the list"**, even while its own table lists **Mini 6 2021 at ৳787**. This is an internally contradicted comparative-price claim, not a retrieval failure.

## Nine-question comparative interpretation

| Question | Qwen | Gemini | Provisional evidence-level assessment |
|---|---|---|---|
| Q1: What is it? | Certain it is only a two-pack glass screen protector, not a case | Certain it is only a two-pack glass screen protector, not a case | Both infer plausible glass protector identity from imagery, but title and Bengali `What's in the box` use 'case/cover'. Product packaging is **ambiguous**; categorical exclusion of a case is not proven. |
| Q2: Compatibility | Broad family list, including images/diagram showing Pro 12.9, Pro 13 and Air 13; gives A16 variant | Broad family list and model numbers; A16 listed | Separate seller's advertised models from **available selected SKU** and physical fit. The image chart (pages 3–4 of PDF) includes some models not offered as distinct color options. An A16-dedicated option is explicitly selectable. |
| Q3: Paperlike? | Says no, glossy clear glass | Says no, glossy clear glass | Reasonable reading of visual seller advertising, not an independently measured surface test. |
| Q4: What will not fit? | Claims unlisted newer M5 Pro/mini 7 and other models won't fit | Claims 12.9/13, older mini and other models won't fit because options not present | Both extrapolate real-world incompatibility from **absence of matching SKU choices**, beyond direct website evidence. Qwen's chart covers some Pro 12.9/13 models while Gemini excludes them; this reflects a distinction between *advertised diagram* and *selectable variants* rather than a proven factual contradiction in shipped products. |
| Q5: Apple Pencil? | Claims Pencil 1st/2nd gen works on top, glossy feel | Claims Pencil works on glass and slippery feel | **No explicit Apple Pencil verification** in user PDF. Actual compatibility/performance claims remain unsupported by inspected site evidence. |
| Q6: Initial price | ৳872 for Pro 11 M4 | Same | Both substantiated by captured initial state. |
| Q7: Stock? | 'Yes — in stock' from enabled cart operations | 'Yes — in stock' from enabled buttons | **Shared unsupported stock inference.** Qwen searched serialized data for a stock field and returned `stockSample: none`; Gemini's browser query returned an empty stock label but enabled button. Neither established an explicit inventory fact. This does not prove out-of-stock. |
| Q8: Features/specifications | PET? No: Qwen cites tempered glass/marketing layers and No Brand structured fields, extra assertions about performance | Likewise claims glass layering/marketing and No Brand | Both inspect images rather than only the sparse dedicated specs. Treat high-definition, protection and layer marketing as **seller claims**, not verified material quality. |
| Q9: Variant change | 11 options, correct A16 price/URL, but wrongly calls A16 cheapest | 11 options, correct A16 price/URL | Both achieved requested interaction and pricing; Qwen's **price-ranking claim is demonstrably wrong** even by its own recorded table. |

## Mechanisms suggested by the trace

1. **Inference without explicit positive stock evidence**, repeated across P1 and P2 for both setups (a recurring *observed behavior*, not an estimated rate).
2. **Negative-evidence overreach**: treating an option not listed as proof a model cannot physically work.
3. **Package-content certainty** despite conflicting seller title/Bengali box wording versus images.
4. **Image-grounded improvement in retrieval**: unlike P1, both downloaded/viewed images, and their responses include diagrams and layered-product descriptions. This is a plausible explanation, **not causally proven**: P2 itself differs from P1.
5. **Qwen internal consistency error**: `৳856` 'cheapest' while the same answer lists `৳787`.
6. **Boundary of measured variables**: both use distinct browser approaches and additional shell/image tools; comparing them as pure model capabilities is invalid.

## Limits and next task

- Only one observed shopping run per agent on P2; no blinded, independently adjudicated human reference. No accuracy, false-negative, calibration, retrieval-rate or cross-model winning percentages.
- Preserve unchanged raw tool responses in the user's private workspace; exported JSON includes tool outputs but not the pixels of external downloaded marketing images. Reconstruct exact visual reads only if original image files are separately preserved.
- Our P2 PDF was captured hours before the agent sessions. Do not score changing prices/stock with an older state.
- Next: run **P3** on both agents in fresh sessions with the same naturalistic shopping prompt adapted to a *foldable iPad case* and target `iPad Air 4 5 6 7 11`; export original traces. Follow with a cross-case review and human adjudication, not a premature generalization.
