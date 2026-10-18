# P1 — Browser tool trace audit (Qwen/OpenCode vs Gemini/Antigravity)

**Status:** Reconstructed from user-supplied original session exports on 2026-10-18. **Not a formal accuracy score or independent human ground truth.**

## Source material (not committed)

- OpenCode: uploaded `p1-qwen.json` (session `ses_eb2051eefffeGH0iz33DxEbmho`); user-reported Qwen3.8-27B Medium is verified by export: model `qwen/qwen3.8-27b`, provider `openrouter`, variant `medium`, OpenCode v1.19.3.
- Antigravity: uploaded `p1-gemini.json` and `p1-gemini.jsonl` (same session content represented in different formats); `gemini.json` and `gemini.jsonl` are **byte-for-byte duplicates** of their matching P1 files; session `183b6f8e-31a5-4b5e-91b1-d2e1894e3210`, model named `Gemini 3.8 Flash (Medium)` by session info.
- Both received substantively the same natural-language shopping prompt. User-supplied transcripts may include credentials, local paths, reasoning metadata and unrelated later export requests. **Do not publish or commit raw traces without redaction and approval.**

## Actual browser operation counts

| | OpenCode/Qwen | Antigravity/Gemini |
|---|---|---|
| Successful Playwright interactions | **9**: navigate 1, snapshot 1, evaluate 6, click 1 | **14**: navigate 1, evaluate 13 |
| Failed browser actions | 0 recorded | **1** initial navigate: `ECONNREFUSED 127.0.0.1:9222` |
| Environment recovery | None in evaluated session | Many setup/diagnostic shell and file calls; launched headless Chromium with CDP on port 9222; subsequent navigate succeeded |
| Explicit screenshot capture of product images | **0** | **0** |
| Browsed full set of selector options individually | **No** | **Yes** |
| Purchase actions | None observed | None observed |
| Recorded usage | OpenCode cost **$0.02855148**; input 28,267, output 2,440, reasoning 2,471, cache-read 219,264 (export's aggregates) | No comparable verified price metadata in supplied transcript |
| Observation times | Session approximately **13:47** local | Browser recovered and worked approximately **13:56–13:59** local |

Antigravity's session also includes later user turns asking where and how to export its transcript. Those later steps are **not part of the shopping experiment**.

## Variant question: what evidence did each agent actually get?

**Qwen:** DOM snapshot contained product title and description, including `For iPad Pro 12.9 (2022/2021/2020/2018)`. DOM inspection identified **five** thumbnail-based `sku-variable-img-wrap` choices but did not expose option names from the thumbnails. A limited search of embedded script text revealed some SKU metadata; the returned snippet did not enumerate all five options. It clicked **only** the second option (Pro 10.5) and observed the correct new price `৳1,357`. Nevertheless its final answer incorrectly treated a general `iPad 9/8/7` model claim as a selectable variant and asserted that Pro 12.9 was not offered as a variant. The original Qwen trace does **not** demonstrate that it read every variant label.

**Gemini:** Playwright `browser_evaluate` gathered five selector elements and used DOM `.click()` on each in sequence; returned observations:
1. `CHINA For iPad Pro 11` — ৳1,567
2. `CHINA For iPad Pro 10.5` — ৳1,357
3. `CHINA For iPad mini 6` — ৳1,357
4. `CHINA For iPadPro 12.9` — ৳1,671
5. `CHINA For iPad Air 5 4` — ৳1,567

It then reselected Pro 10.5 and observed the SKU URL ending `-s1869233426.html` and the changed price.

**Inference:** This is strong support for a **coverage/evidence-use error in Qwen's final variant list**, not evidence that Pro 12.9 was inaccessible through its browser tool. However, the agents loaded the site several minutes apart, potentially in different browser profiles; there is no common frozen page state, so avoid fully attributing the difference to model weights.

## Stock question: both inferred more than the page supports

- Qwen explicitly queried stock: `stockTexts: []` and `soldOut: false`, yet final response asserted the product was 'in stock.'
- Gemini queried `stockInfo: ""` and subsequently observed `Buy Now`/`Add to Cart` with `disabled: false`, yet asserted it was in stock and ready to order.

Both agents **observed an absence of explicit stock text (in inspected scope) and made a confident stock inference from purchasing affordances**. This identifies an interpretation/inference pattern more precisely than the final answers alone. It does **not** establish that inventory was actually zero or that either agent's binary stock answer was false.

## Claims not corroborated by the trace

- **Image-only wording:** Neither agent invoked `browser_take_screenshot` or another confirmed image-pixel inspection tool during the shopping task. Qwen received accessibility snapshot text; Gemini obtained product image URLs and rendered DOM text. The user-captured full-page PDF contains a marketing image using restrictive `Only compatible with` wording; this wording was **not present in either recovered browser transcript**. Both agents' negative compatibility answers therefore lack that relevant *image-only* evidence.
- **Gemini technical elaboration:** The answer stated that certain newer iPads had different magnetic polarities and inferred additional incompatibilities; no corresponding page evidence was found in its recorded browsing outputs. Avoid labeling the true engineering claim false without external verification; it is **unsupported as a website-grounded claim**.
- **Pencil claims:** Page marketing says drawing, note-taking, precision and nib life; treating that as independently verified Apple Pencil model support/performance goes beyond the recorded site evidence.

## Implications for the next runs

1. Preserve current P1 outputs and traces unchanged; record this analysis separately.
2. In future runs, freeze browser configuration (Playwright MCP version, Chromium version/profile, viewport, locale/location), record exact timestamps and session states, and obtain raw snapshots and images.
3. Keep the *same normal shopping prompt* across agents; do **not** reveal the research goals or negative-evidence scoring rubric to either agent.
4. For the naturalistic baseline, let each agent decide how thoroughly to browse. Record whether it inspected images or clicked all variants as part of the measured behavior, rather than retroactively requiring it.
5. Consider a *separate predeclared controlled-access condition* later, in which each agent is given the same frozen evidence or an identical fixed set of browsing actions. Do not mix its results with the naturalistic baseline.

## Classification (qualitative only)

- Qwen Q2/Q4: **failure to distinguish listing-level compatibility from observed selectable SKUs**; not established as a browser-access failure.
- Both Q7: **unsupported positive inventory inference** based on buttons/no-sold-out text; not a confirmed factually false stock claim.
- Both Q4: **unsupported blanket exclusions** from available listing/model mentions; access to restrictive marketing image text not documented.
- Gemini Q4: **unverified technical rationale** added beyond website evidence.
- Both Q6/Q9: **correctly captured price and requested Pro 10.5 variant change** in corresponding browser states.
