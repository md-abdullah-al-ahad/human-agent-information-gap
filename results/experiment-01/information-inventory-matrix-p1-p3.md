# Information Inventory & Accessibility Matrix (Pilot P1–P3)

**Status:** Primary empirical dataset for Stage 1 / Experiment 01.  
**Framework:** 4-Stage Human–Agent Information Accessibility Pipeline.  
**Scope:** Three pilot pages from Daraz Bangladesh audited across Human Capture (PDF/Browser), Tool Exposure (Playwright MCP), Agent Retrieval (Qwen 3.8 27B vs Gemini 3.8 Flash), and Final Agent Output.

---

## 1. The 4-Stage Information Pipeline Model

Every discrete unit of website information traverses four operational boundaries:

```
[Stage 1: Website & Human Surface] 
  (Rendered text, structured fields, in-image graphics, interactive states)
       │
       ▼  GAP 1: Tool Exposure Barrier (What Playwright/DOM/Scraper exposes)
[Stage 2: Tool-Exposed Information]
  (Accessibility tree, DOM snapshot, evaluate scripts, image file downloads)
       │
       ▼  GAP 2: Agent Exploration & Retrieval Barrier (What the agent actually inspects)
[Stage 3: Agent-Retrieved Information]
  (Content present in the agent's context and tool outputs)
       │
       ▼  GAP 3: Output Reporting & Inference Barrier (What the agent conveys vs. invents)
[Stage 4: Final Reported Information]
  (Faithfully reported, omitted, or converted into unsupported inferences)
```

---

## 2. Product P1: ESR Magnetic Paper-Feel Screen Protector

- **Page URL:** `https://www.daraz.com.bd/products/ipad-pro-11-129-esr-ipad-9-8-7-ipad-mini-6ipad-air-5-air-4-i373818784.html`
- **Initial State:** `CHINA For iPad Air 5 4` (৳1,567)
- **Alternate State:** `CHINA For iPad Pro 10.5` (৳1,357)

| Item # | Information Item | Surface / Modality | Stage 1: Human-Visible | Stage 2: Tool-Exposed | Stage 3: Qwen Retrieved | Stage 3: Gemini Retrieved | Stage 4: Qwen Reported | Stage 4: Gemini Reported | Observed Gap / Barrier |
|---|---|---|---|---|---|---|---|---|---|
| P1-01 | Listing Title & Main Product Identity | Rendered DOM text | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported correctly | Reported correctly | None (Plain text accessible) |
| P1-02 | Marketplace Brand Header (`No Brand`) | Structured DOM field | Yes (PDF p. 1) | Yes (DOM text) | Yes | Yes | Reported (`No Brand`) | Reported (`No Brand`) | None |
| P1-03 | Seller Brand Claim in Details (`ESR`) | Expanded detail text | Yes (PDF p. 2) | Yes (DOM text) | Yes | Yes | Reported (`ESR`) | Reported (`ESR`) | Internal seller conflict preserved |
| P1-04 | Initial Selected Variant Price (`৳1,567`) | Dynamic DOM text | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported correctly | Reported correctly | None |
| P1-05 | Initial Strike-through Price (`৳1,881`, -17%) | Dynamic DOM text | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported correctly | Reported correctly | None |
| P1-06 | Purchase Buttons Enabled State | Interactive UI button | Yes (PDF p. 1) | Yes (`disabled: false`) | Yes | Yes | Used to claim "in stock" | Used to claim "in stock" | **Gap 3 (Affordance Overreach)**: Empty stock text converted to confident positive stock claim |
| P1-07 | Explicit Inventory / Stock Count | Dedicated text field | **Not present on page** | **Empty string / null** | Checked (`stockTexts: []`) | Checked (`stockInfo: ""`) | Concluded: "In stock" | Concluded: "In stock" | **Gap 3**: Both agents failed to report that stock data is absent from page |
| P1-08 | Alternate Variant Click (`Pro 10.5`) | Interactive UI click | Yes (Live browser) | Yes (DOM click) | Yes (1 click) | Yes (1 click) | Selected successfully | Selected successfully | None (Interactive navigation succeeded) |
| P1-09 | Alternate Variant Displayed Price (`৳1,357`) | Dynamic DOM update | Yes (Live browser) | Yes (DOM text) | Yes | Yes | Reported correctly | Reported correctly | None |
| P1-10 | Full Selectable Variant Roster (5 options) | Selector thumbnails | Yes (PDF p. 1) | Yes (DOM elements) | **Partial** (clicked only 1, inspected script) | **Complete** (iterated DOM click loop across all 5) | **Omitted Pro 12.9; mislisted 9/8/7 as selectable SKU** | **Correctly enumerated all 5 SKUs** | **Gap 2 (Agent Exploration)**: Qwen did not iterate all thumbnails; conflated title text with selectable SKUs |
| P1-11 | Restrictive Compatibility Statement ("Only compatible with...") | **In-Image Graphic** (PDF p. 2) | Yes (Visible to human eye) | **Omitted from DOM / text snapshot** | **Not retrieved** (no image downloaded or OCR'd) | **Not retrieved** (no image downloaded or OCR'd) | Inferred exclusions without evidence | Inferred exclusions + invented "magnetic polarity" rationale | **Gap 1 & Gap 2 (Image Barrier)**: Crucial restrictive text embedded in image pixels was completely invisible to text snapshots |
| P1-12 | Surface Feel Claim ("Paper-Feel", drawing texture) | Title text + Image graphics | Yes (PDF pp. 1, 4–7) | Yes (in title / text) | Yes | Yes | Reported ("paper-feel") | Reported ("paper-feel", anti-glare) | Gemini added unevidenced anti-glare / reflection claims (Gap 3) |
| P1-13 | Material Specification (`PET`) | Dedicated spec table | Yes (PDF p. 2) | Yes (DOM text) | Yes | Yes | Reported (`PET`) | Reported (`PET`, "high-grade") | None |
| P1-14 | Stylus / Apple Pencil Support | Marketing text/graphics | Yes (Writing/drawing ads) | Yes (in description) | Yes (seller claims) | Yes (seller claims) | Asserted verified Apple Pencil support | Asserted verified support + specific tip-wear claims | **Gap 3 (Claim-to-Fact Overreach)**: Converted seller marketing claims into verified hardware compatibility |

---

## 3. Product P2: 2PCS Glass Screen Protector

- **Page URL:** `https://www.daraz.com.bd/products/-i567669430.html`
- **Initial State:** `Color: Pro 11 M4`, `Keyboard language: 2PCS` (৳872)
- **Alternate State:** `For iPad A16 2025` (৳856)

| Item # | Information Item | Surface / Modality | Stage 1: Human-Visible | Stage 2: Tool-Exposed | Stage 3: Qwen Retrieved | Stage 3: Gemini Retrieved | Stage 4: Qwen Reported | Stage 4: Gemini Reported | Observed Gap / Barrier |
|---|---|---|---|---|---|---|---|---|---|
| P2-01 | Listing Title ("2PCS Screen Protector Case ... Cover") | Plain text DOM | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported title | Reported title | Ambiguous seller title |
| P2-02 | Physical Form Factor (Glass protector, NOT a case) | Image graphics + text | Yes (PDF pp. 2, 4) | Yes (Images downloaded) | Yes (viewed images) | Yes (viewed images) | Categorically stated "No case" | Categorically stated "No case" | Disambiguation successful via image tool, but package ambiguity was flattened |
| P2-03 | Package Contents ("What's in the box" Bengali text) | Expanded detail text | Yes (PDF p. 5) | Yes (View More expanded) | Yes | Yes | Partially noted | Read via `browser_evaluate` | None |
| P2-04 | Initial Displayed Price (`৳872`, -62%) | Dynamic DOM text | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported correctly | Reported correctly | None |
| P2-05 | Purchase Buttons Enabled State | Interactive UI button | Yes (PDF p. 1) | Yes (`disabled: false`) | Yes | Yes | Claimed "In stock" | Claimed "In stock" | **Gap 3 (Affordance Overreach)**: Inferred stock from active button |
| P2-06 | Explicit Inventory / Stock Field | Dedicated field | **Not present on page** | **`stockSample: none` / empty** | Checked (none found) | Checked (empty label) | Claimed "In stock" | Claimed "In stock" | **Gap 3**: Ignored absence of positive evidence |
| P2-07 | Alternate Variant Click (`For iPad A16 2025`) | Interactive UI click | Yes (Live browser) | Yes (DOM click) | Yes | Yes | Selected successfully | Selected successfully | None |
| P2-08 | Alternate Variant Displayed Price (`৳856`) | Dynamic DOM update | Yes (Live browser) | Yes (DOM update) | Yes | Yes | Reported correctly | Reported correctly | None |
| P2-09 | Full Selectable Variant Roster (11 options) | Dropdown / option wraps | Yes (PDF p. 1) | Yes (`window.__moduleData__` / DOM) | Yes (11 SKUs extracted) | Yes (11 SKUs clicked) | Correctly extracted all 11 option names & prices | Correctly extracted all 11 option names & prices | None (Both agents thoroughly inspected selector) |
| P2-10 | Variant Price Hierarchy (Mini 6 is lowest at ৳787) | Structured selector data | Yes (Visible across options) | Yes (Extracted in table) | Yes (Extracted ৳787) | Yes (Extracted ৳787) | **Asserted A16 (৳856) is "the cheapest variant"** | Reported accurate price list | **Gap 3 (Internal Contradiction)**: Qwen contradicted its own extracted table in final text |
| P2-11 | Detailed Model Compatibility Chart | **In-Image Diagram** (PDF pp. 3–4) | Yes (Lists Pro 12.9, Pro 13, Air 13, etc.) | **Image pixels downloaded via shell** | Downloaded & called image read | Downloaded & called image view | Referenced model families from chart | Referenced model families from chart | Visual retrieval succeeded when agents used shell downloads + image tools |
| P2-12 | Unlisted Models Exclusion (M5 Pro, unlisted sizes) | Negative scope | **Not stated on page** | **Not stated in DOM** | Not stated | Not stated | Asserted unlisted models "will not fit" | Asserted unlisted models "will not fit" | **Gap 3 (Negative Overreach)**: Absence of SKU option transformed into verified physical incompatibility |
| P2-13 | Five-Layer Glass Construction | In-Image Graphic (PDF p. 2) | Yes (Layered diagram) | Downloaded image | Viewed image | Viewed image | Cited layer marketing | Cited layer marketing | None (Retrieved from visual asset) |
| P2-14 | Stylus / Apple Pencil Support | Page scope | **Not present on page** | **Not in text or images** | Not found | Not found | Claimed Pencil 1st/2nd gen works smoothly | Claimed Pencil works on glass | **Gap 3 (Extrapolation)**: Unverified performance claims added without page evidence |

---

## 4. Product P3: 3+Y-fold Clear iPad Folio Case

- **Page URL:** `https://www.daraz.com.bd/products/-i567663291.html`
- **Initial State:** `Color: YZ-YKL Black`, `Size: iPad Pro 11 2018-22` (৳1,223)
- **Alternate State:** `Color: YZ-YKL Black`, `Size: iPad Air 4 5 6 7 11` (৳1,217)

| Item # | Information Item | Surface / Modality | Stage 1: Human-Visible | Stage 2: Tool-Exposed | Stage 3: Qwen Retrieved | Stage 3: Gemini Retrieved | Stage 4: Qwen Reported | Stage 4: Gemini Reported | Observed Gap / Barrier |
|---|---|---|---|---|---|---|---|---|---|
| P3-01 | Product Identity (Protective Case, NOT screen protector) | Text title + Image graphics | Yes (PDF pp. 1–5) | Yes (DOM + Images) | Yes | Yes | Correctly identified folio case | Correctly identified folio case | None |
| P3-02 | Protective Transit Film Instruction ("Peel off film on inner/outer case") | Expanded text / Image | Yes (PDF p. 5) | Yes (DOM text) | Yes | Yes | Correctly identified case film (no screen protector) | Correctly identified case film (no screen protector) | None (Contextual disambiguation succeeded) |
| P3-03 | Initial Displayed Price (`৳1,223`, -60%) | Dynamic DOM text | Yes (PDF p. 1) | Yes (Snapshot) | Yes | Yes | Reported correctly | Reported correctly | None |
| P3-04 | Purchase Buttons Enabled State | Interactive UI button | Yes (PDF p. 1) | Yes (`disabled: false`) | Yes | Yes | Claimed "In stock" | Claimed "In stock" | **Gap 3 (Affordance Overreach)**: Clickable button treated as verified warehouse stock |
| P3-05 | Explicit Stock Quantity / Status | Dedicated text field | **Not present on page** | **Empty string / null** | Checked (none found) | Checked (none found) | Claimed "In stock" | Claimed "In stock" | **Gap 3**: Ignored lack of inventory data |
| P3-06 | Alternate Size Click (`iPad Air 4 5 6 7 11`) | Interactive UI click | Yes (Live browser) | Yes (DOM click) | Yes | Yes | Selected successfully | Selected successfully | None |
| P3-07 | Alternate Size Displayed Price (`৳1,217`) | Dynamic DOM update | Yes (Live browser) | Yes (DOM update) | Yes | Yes | Reported correctly | Reported correctly | None |
| P3-08 | Full Size Option Roster (10 sizes) | Size selector elements | Yes (PDF p. 1) | Yes (DOM elements) | Yes (10 sizes listed) | Yes (10 sizes listed) | Reported size names | Reported size names | None |
| P3-09 | Full Color Option Roster (6 colors) | Color selector elements | Yes (PDF p. 1) | Yes (DOM elements) | Yes | Yes | Reported color names | Reported color names + price matrix | None |
| P3-10 | Material Claims (PU leather, TPU, PC back, microfiber) | Text + Marketing graphics | Yes (PDF pp. 2–5) | Yes (DOM + Images) | Yes | Yes | Reported materials | Reported materials + "air cushion" marketing | None |
| P3-11 | Physical Stylus Channel in Case Frame | **Pure Visual Feature in Images** (PDF pp. 2, 4) | Yes (Channel along tablet edge visible to eye) | **Image files downloaded via shell** | Downloaded images | Downloaded images | **Reported "No Pencil support or slot found"** | **Asserted molded Pencil slot, push-out hole, left-side placement** | **Gap 1 / Gap 3 Discrepancy**: Visual feature exists without accompanying text; Qwen relied on text absence, Gemini extrapolated unverified functional details |
| P3-12 | Apple Pencil Magnetic Charging Support | Page scope | **Not present on page** | **Not stated in text** | Not found | Not found | Correctly noted absence of charging claim | Asserted wireless charging limitations without page proof | **Gap 3 (Unverified Elaboration)**: Gemini invented technical charging mechanics |
| P3-13 | Unlisted Models Exclusion (Pro 12.9, older mini) | Negative scope | **Not stated on page** | **Not stated in DOM** | Not found | Not found | Asserted unlisted models "cannot fit" | Asserted unlisted models "cannot fit" + chassis rationale | **Gap 3 (Negative Overreach)**: Converted lack of selectable SKU into physical incompatibility |

---

## 5. Cross-Case Summary of Gaps

Across all 41 audited information items on P1, P2, and P3:

1. **Plain Text & Structured DOM Elements (Stage 1 -> Stage 4)**:
   - **Retention Rate: Very High (>95%)**. Product titles, basic prices, seller names, and standard descriptions reliably survived from website to agent output.
2. **Interactive UI State & Pricing (Stage 1 -> Stage 4)**:
   - **Retention Rate: 100%**. Both agents successfully executed Playwright clicks to switch variants and retrieved the dynamic price updates (`Pro 10.5` at ৳1,357; `A16` at ৳856; `Air case` at ৳1,217).
3. **In-Image Critical Information (Gap 1: Tool Exposure Barrier)**:
   - When text was baked into images (such as P1's restrictive *"Only compatible with..."* notice or P2's model compatibility matrix), standard Playwright snapshots and markdown scrapers suffered a **100% retrieval omission**. Information was only recovered when agents took extra actions to shell-download image files and invoke vision tools.
4. **Pure Visual Features Without Accompanying Text (Gap 1 / Gap 3 Discrepancy)**:
   - The P3 stylus channel demonstrates that visual-only affordances create severe agent divergence: one agent treated the absence of descriptive text as complete absence of the feature (Qwen), while the other identified the visual recess and extrapolated unverified physical behaviors like push-out holes and charging limits (Gemini).
5. **Absence of Evidence vs. Negative Fact (Gap 3: Inference Overreach)**:
   - **Stock Availability**: 6 out of 6 runs exhibited affordance overreach (asserting "in stock" from clickable purchase buttons despite empty stock data).
   - **Compatibility Exclusions**: Both agents repeatedly treated the absence of an option in a dropdown menu as proof of physical incompatibility with real hardware.
