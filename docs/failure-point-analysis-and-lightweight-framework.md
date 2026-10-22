# Failure Point Analysis & Lightweight Web Extraction Framework (LWA-Web)

**Authors:** Empirical AI & Agent Research Group
**Benchmark Reference:** 15-platform collected dataset (1,010 agent-item rows across 323 researcher-annotated item IDs; prospective preregistration and independent human adjudication are not established for every item)
**Date:** 2026-10-20
**Core Objective:** Conduct a rigorous root-cause failure point analysis of modern web architectures under autonomous agent interaction, and formulate a high-efficiency, lightweight framework to resolve information gaps with minimal token usage and low latency.

---

## 1. Introduction: The Web Agent Dilemma

Modern autonomous web agents face an acute operational dilemma when interacting with production web interfaces:

1. **The Heavy Browser Tax (Playwright / Puppeteer + VLM)**:
   - Captures high-fidelity dynamic DOM and full-page screenshots.
   - **Cost & Latency Barrier**: Some recorded browser-agent runs were lengthy and costly; these ranges are not measured consistently across the whole dataset.
   - **Downsampling Blindness**: A 10,000-pixel full-page screenshot downscaled into standard VLM vision tokens (e.g., 1024x1024 or 768x768) renders critical text (discounts, terms, dates) illegible due to pixel compression.

2. **The Static Scraping Trap (cURL / HTTP Requests + Text LLM)**:
   - A single HTTP request may be fast, but complete agent sessions include follow-up retrieval and reasoning.
   - **Hydration Gap**: Some initial HTML responses omit content later rendered by JavaScript. The claimed 19.2-point accuracy drop is withdrawn because the master CSV has uncoded and disputed scores.
   - **The Compensatory Loop**: When faced with missing data, unconstrained agents trigger explosive bash/scripting loops (downloading 80+ JavaScript chunks, executing 1,400+ terminal steps), resulting in **7.01x latency surges** and API budget exhaustion.
   - **Total Visual Blindness**: Zero access to text trapped inside raster banner pixels or CSS background images.

The proposed **Lightweight Agentic Web Extraction Framework (LWA-Web)** explores ways to reduce these barriers. The current code is a fixture-based prototype, not a validated replacement for full browser automation.

---

## 2. Empirical Failure Point & Root Cause Analysis

The 1,010 rows across 15 platforms suggest seven candidate failure points. The rows are not 1,010 independent facts or uniformly adjudicated successes.

```
+----------------------------------------------------------------------------------------------------+
|                                    TAXONOMY OF FAILURE POINTS                                      |
|                                                                                                    |
| [FP-1] Raster Pixel Sequestration & CSS Background Trapping (Visual Blindness)                     |
| [FP-2] Client-Side Hydration & Skeleton Asymmetry (Structural Blindness)                           |
| [FP-3] The Compensatory Scraping Loop & Inverted Economics (Algorithmic Divergence)               |
| [FP-4] DOM Bloat & Context Window Congestion (Token Inefficiency)                                  |
| [FP-5] Alt-Text Truncation & Unlabeled Entity Grounding (Semantic Flattening)                      |
| [FP-6] Affordance Overreach on Silent Omission (Hallucinated Inferences)                           |
| [FP-7] Edge Anti-Bot & TLS Verification Barriers (Access Denials)                                  |
+----------------------------------------------------------------------------------------------------+
```

### FP-1: Raster Pixel Sequestration & CSS Background Trapping (Visual Blindness)
- **Root Cause**: Marketing departments and frontend designers flatten critical commercial and contractual data into raster image files (`.webp`, `.jpg`, `.png`) or CSS inline styles (`background-image: url(...)`), while leaving DOM `alt` attributes empty or purely generic (e.g., `alt="ACI Banner"`, `alt="Nagad Offer"`).
- **Empirical Evidence**:
  - *Shwapno Online (`BD-QC02`)*: Primary checkout coupons `PUJA6` (6% off up to ৳150) and `PUJA7` (7% off up to ৳200) had **0 textual occurrences** in the 2.4 MB DOM payload.
  - *Nagad (`BD-FN02`)*: Weekend transaction threshold (৳8,880) and bonus (৳80) were embedded exclusively inside inline background graphics.
  - *bKash (`BD-FN01`)*: Mastercard instant cashback percentages and partner terms existed solely as pixel glyphs.
- **Agent Failure Mechanism**:
  - Text-based agents perceive total data absence and fail.
  - Full-page vision agents downsample the 10,000px page, turning the text into illegible artifacts unless expensive multi-turn sub-crops are executed.

### FP-2: Client-Side Hydration & Skeleton Asymmetry (Structural Blindness)
- **Root Cause**: Next.js (Turbopack), Angular SSR, and React hydrate data dynamically via client-side JavaScript execution (Algolia search queries, Firebase, GraphQL). The initial server HTML is an empty skeleton.
- **Empirical Evidence**:
  - *Bdjobs (`BD-CL02`)*: Live job vacancy counts are injected via a client-side typewriter script. Static DOM contains only `<span id="typewriter"></span>`.
  - *Shwapno (`BD-QC02`)*: Off-screen deal carousels render placeholder shimmer divs (`div.img-shimmer`) until scrolled or hydrated.
  - *US-Bangla (`BD-TR03`)*: Origin airport dropdowns require client-side AJAX execution to render station options.
- **Agent Failure Mechanism**: Static scrapers extract empty placeholders, leading to false negative reports or ungrounded guesses.

### FP-3: The Compensatory Scraping Loop & Inverted Economics (Algorithmic Divergence)
- **Root Cause**: When an autonomous agent with shell access encounters unhydrated or missing DOM data, its objective function drives it to search for alternative extraction pathways without an economic stop condition.
- **Empirical Evidence**:
  - *Bdjobs (`BD-CL02`)*: OpenCode without Playwright downloaded 82 client JS chunks, executed 1,484 terminal steps, and exhausted the OpenRouter $2.01 credit limit without completing the audit.
  - *Shwapno (`BD-QC02`)*: OpenCode without Playwright required 617 seconds (10.28 minutes) vs. 88 seconds with Playwright (**7.01x latency surge**), executing dozens of ImageMagick crop passes and regex parsers.
  - *Nagad (`BD-FN02`)*: Latency surged from 9.47 minutes to 23.83 minutes (**2.52x surge**).
- **Agent Failure Mechanism**: In these selected runs, missing content prompted long follow-up retrieval sequences. This does not establish that static retrieval is generally slower or costlier.

### FP-4: DOM Bloat & Context Window Congestion (Token Inefficiency)
- **Root Cause**: Production web pages bundle massive inline scripts (Next.js data bundles, webpack chunks), inline CSS stylesheets, tracking scripts, and deep nested div hierarchies.
- **Empirical Evidence**:
  - Reported raw DOM sizes: Shwapno (2.41 MB), Chaldal (1.78 MB), Nagad (542 KB). Dividing bytes by four gives only a rough token proxy, not tokenizer-measured usage.
  - Sending an entire DOM to an LLM could incur large token costs; saved byte counts alone do not establish actual model context or billing.
- **Agent Failure Mechanism**: Irrelevant markup can make retrieval harder; this dataset has not isolated its effect on answer quality.

### FP-5: Alt-Text Truncation & Unlabeled Entity Grounding (Semantic Flattening)
- **Root Cause**: Real-world visual assets depicting named public entities (brand ambassadors, partner institutions, regulatory seals) lack semantic labeling or alt attributes.
- **Empirical Evidence**:
  - *Nagad (`BD-FN02`)*: A popup figure lacks useful textual identification in the markup. The existing ground-truth label gives two different names, Jamal Bhuyan and Tariq Kazi; identity and associated PASS scores require visual adjudication.
  - *Gov.uk (`S3`)*: Statutory agency partner crests were embedded as unlabelled SVGs.
- **Agent Failure Mechanism**: Pure text scrapers report "Not Found" because no textual signal exists, while multi-modal visual agents ground entity identities directly from facial features and logos.

### FP-6: Affordance Overreach on Silent Omission (Hallucinated Inferences)
- **Root Cause**: An omitted status leaves the answer unknown; it is not evidence of a negative status.
- **Empirical Evidence**:
  - *Star Tech (`S1`)*: Its captured page contains an explicit "In Stock" badge, so this case does not demonstrate stock inferred solely from a purchase button.
  - *Daraz (`P1–P3`)*: Models converted lack of selectable color/size SKUs into claims of technical incompatibility.
- **Agent Failure Mechanism**: LLMs have a strong inductive bias to treat clickable UI affordances as positive verification of backend transactional states.

### FP-7: Edge Anti-Bot & TLS Verification Barriers (Access Denials)
- **Root Cause**: Cloudflare Turnstile, Akamai, and AWS WAF enforce TLS client hello fingerprinting, header consistency checks, and JavaScript challenge evaluation.
- **Empirical Evidence**:
  - *Biman Bangladesh Airlines (`BD-TR02`)*: Static cURL requests were blocked with HTTP 403 Forbidden ("Attention Required! | Cloudflare").
  - *Nagad Asset Host (`BD-FN02`)*: Requests to `https://backend.nagad.com.bd:8443` triggered Cloudflare 403 blocking pages.
- **Agent Failure Mechanism**: Both access paths can be blocked. The saved Biman browser screenshot and DOM show a Cloudflare verification page, not the airline content.

---

## 3. Architecture of the Lightweight Web Extraction Framework (LWA-Web)

The proposed **Lightweight Web Extraction Framework (LWA-Web)** has modules that remain to be implemented and evaluated. No end-to-end accuracy, cost, or latency target has been validated.

LWA-Web operates on a dual-sided architectural paradigm:
1. **Agent-Facing Client Middleware (LiteAgent-Extractor)**: An intelligent preprocessing pipeline that extracts, condenses, and enriches web content before passing it to LLM reasoning.
2. **Server-Facing Publisher Standard (Web-for-Agents Protocol)**: Declarative guidelines and lightweight endpoints for website developers.

```
+----------------------------------------------------------------------------------------------------+
|                                LWA-WEB DUAL-SIDED ARCHITECTURE                                     |
|                                                                                                    |
|   [Target Website]                                                                                 |
|          |                                                                                         |
|          v                                                                                         |
|   +--------------------------------------------------------------------------------------------+   |
|   | 1. Bounded Chromium capture; question-relevant readiness still proposed                   |   |
|   +--------------------------------------------------------------------------------------------+   |
|          |                                                                                         |
|          +--------------------------------------+                                                  |
|          | (DOM Tree)                           | (Asset URLs & Bounding Boxes)                    |
|          v                                      v                                                  |
|   +----------------------------------+   +-----------------------------------------------------+   |
|   | 2. HTML text condenser           |   | 3. Proposed visual micro-triage pipeline            |   |
|   | - Strips <script>, <style>, <svg>|   | - Filters untagged banners/promos (generic/no alt)  |   |
|   | - Emits compact text/links       |   | - Referenced live images fetched within limits      |   |
|   | - Generates compact text         |   | - Optional Tesseract OCR; crops unimplemented       |   |
|   | - Measures output bytes          |   | - Legacy fixtures outside the agent-facing path     |   |
|   +----------------------------------+   +-----------------------------------------------------+   |
|          |                                      |                                                  |
|          +-------------------+------------------+                                                  |
|                              v                                                                     |
|   +--------------------------------------------------------------------------------------------+   |
|   | 4. Deterministic Omission & Affordance Normalizer                                          |   |
|   | - MCP emits unknown states; purchase controls are observed affordances                    |   |
|   +--------------------------------------------------------------------------------------------+   |
|                              |                                                                     |
|                              v                                                                     |
|   +--------------------------------------------------------------------------------------------+   |
|   | 5. Proposed circuit breaker (not implemented)                                             |   |
|   +--------------------------------------------------------------------------------------------+   |
|                              |                                                                     |
|                              v                                                                     |
|   [Bounded evidence JSON plus retrievable local capture handle]                                   |
|                              |                                                                     |
|                              v                                                                     |
|   [LLM Reasoning Agent (Qwen / Gemini / Claude / GPT-4o)]                                          |
|   - Accuracy, latency, and API cost have not been established                                      |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Key Modules of LiteAgent-Extractor

### Module 1: Single-Pass Hydration Runner (Fast Lifecycle)
- **Targeted problems**: FP-2 (hydration asymmetry) and some access barriers. The MCP tool now offers explicitly selected bounded Chromium capture; question-relevant readiness and interactive-state coverage remain future work.
- **Design**: Instead of keeping an open interactive browser session or running static cURL, execute a targeted single-pass headless Chromium fetch using the Chrome DevTools Protocol (CDP) or Playwright.
- **Lifecycle**: Navigates to target, waits for question-relevant content or state to stabilize within a declared timeout, extracts the rendered DOM tree and image bounding boxes, and terminates. `networkidle` alone does not establish that hydration or lazy loading is complete.
- **Execution time**: Not established across the benchmark.
- **Edge compatibility**: Browser automation cannot be assumed to pass Cloudflare or other access controls; Biman's saved browser capture is a challenge page.

### Module 2: HTML Text Condenser
- **Problem Solved**: FP-4 (DOM Bloat & Token Waste).
- **Current implementation**: `scripts/lightweight_web_extractor.py` uses Python's `HTMLParser` to omit script and style content and collect selected text, links, buttons, and image references. It does not parse an AST, collapse wrapper chains, or guarantee retention of all tables and interactive states.
- **Measurement**: Compare input and output bytes for a specific fixture if useful. Byte reduction is not tokenizer-measured savings and says nothing by itself about retained facts.

### Module 3: Selective Visual Micro-Triage & Pixel-to-Text Injection
- **Targeted problems**: FP-1 (in-image text) and FP-5 (unlabeled entities). The following fuller micro-triage design is only partly implemented.
- **Proposed design**:
  1. The condenser inspects all `<img>` and visual elements in the DOM.
  2. It identifies candidate trapped images using heuristics:
     - Missing or generic alt attributes (`alt=""`, `alt="ACI Banner"`, `alt="Nagad Offer"`).
     - Promotional keywords in class names or URLs (`banner`, `slider`, `offer`, `coupon`, `promo`).
     - High aspect ratio hero elements.
  3. Crop candidate images instead of submitting an entire screenshot to a vision model.
  4. It executes fast localized OCR (or calls a lightweight micro-vision model on just that 200x100 crop).
  5. The extracted text is injected directly into the semantic markdown tree:
     ```markdown
     [IMG alt='ACI Banner' data-trapped-text="স্বপ্ন অনলাইনে পূজার সাশ্রয় | PUJA6: 6% off up to ৳150 | PUJA7: 7% off up to ৳200" src='slider_1_puja.webp']
     ```
- **Current implementation**: The old fixture extractor has manually entered text in an asset-name lookup table, but is outside the agent-facing MCP path. The MCP tool can automatically fetch at most three live-page `<img>` or inline CSS-background raster references and run Tesseract OCR on their pixels if the binary and English/Bangla data are available. It records image bytes, hash, source URL, and OCR line coordinates. OCR lines are unverified candidates and cannot alone pass `check_claim`. It does not discover external stylesheet backgrounds, crop screenshots by rendered geometry, identify people, or prove that an asset was visible in the human viewport. A user-local Tesseract runtime could not read the exact `PUJA6`/`PUJA7` codes from the saved Shwapno crop, so that mitigation remains unverified on this case. A fresh agent answered from one pre-generated Shwapno document; its published 20/20 assessment was not independently exact-match adjudicated and it did not call the MCP tool.

### Module 4: Deterministic Omission & Affordance Normalizer
- **Targeted problem**: FP-6 (affordance overreach). The MCP tool returns an unknown state for stock/compatibility questions without bound explicit evidence. Its `check_claim` tool confirms exact source quotations only and abstains on semantic claims.
- **Proposed design**:
  - The condenser audits interactive buttons and transactional cards.
  - If a product card has an active `[BUTTON: Buy Now]` but no explicit stock field in the **inspected scope**, return `stock_status=unknown` and cite the button only as an observed affordance. Do not describe the full page or actual inventory as explicitly unstated unless the relevant scope was fully inspected.
  - The agent-facing evidence contract requires explicit support for an `in_stock` or `out_of_stock` claim; an enabled control is insufficient.
- **Status**: No agent follow-up test establishes that this note prevents unsupported inventory claims. The absence of stock text in a parsed fragment also does not prove absence from the whole site.

### Module 5: Autonomous Circuit-Breaker Guardrail
- **Targeted problem**: FP-3 (the compensatory loop). This is not implemented.
- **Design**:
  - In an autonomous agent environment, enforces a hard policy budget:
    - Maximum terminal bash commands per retrieval query: 3 steps.
    - If data is not resolved within 3 steps, the agent is forced to emit a structured `MISSING_FIELD` response rather than downloading arbitrary client bundles.
- **Status**: The proposed budget policy has not been evaluated; it may also reduce information retrieval if stopped too early.

---

## 5. Publisher-Side Protocol: The Web-for-Agents Standard

To enable websites to become natively agent-accessible without forcing agents to reverse-engineer client code, we propose three publisher-side design ideas. These are not established web standards or evaluated interventions:

1. **Pixel-to-Text Parity Requirement**:
   - Any promotional code, monetary threshold, delivery guarantee, or legal disclaimer rendered inside an image must be mirrored in a structured attribute:
     ```html
     <img src="puja_banner.webp"
          alt="Shwapno Puja Savings: 6% off with code PUJA6 (min 1000Tk, max 150Tk); 7% off with code PUJA7 (min 1500Tk, max 200Tk)"
          data-agent-promo="PUJA6:6%:150;PUJA7:7%:200">
     ```
2. **Standard Agent Discovery Endpoint (`/.well-known/agent-manifest.json` / `llms.txt`)**:
   - Provide a lightweight machine-readable manifest exposing core transactional endpoints (product search, store hours, coverage areas, helplines).
3. **Explicit State Declarations**:
   - Never rely on visual color coding or button states alone to communicate operational state. Always provide explicit semantic text:
     `<span class="badge" data-stock="in_stock">In Stock</span>`.

---

## 6. Implementation Status

The existing [fixture extractor](../scripts/lightweight_web_extractor.py) and legacy `extract_web_page` function condense selected saved or fetched HTML. Their known-image annotations are manually supplied fixtures, and their benchmark cache is explicitly enabled and potentially stale. The legacy function is no longer registered as an agent-facing MCP tool. The newer `inspect_web_evidence` tool uses the [evidence core](../scripts/lwa_evidence.py) for explicit snapshot/live-HTTP modes, optional bounded Chromium rendering, provenance, challenge detection, extractor views, embedded JSON, passive browser JSON, and unknown states. It can fetch a few referenced live raster assets for OCR when Tesseract is installed; snapshot OCR requires explicit local image paths. The [capture store](../scripts/lwa_evidence_store.py) supports `inspect_evidence`, bounded `inspect_image_crop`, and an exact-quotation-only `check_claim`. Verified interactive coverage, reliable entity binding, general semantic claim checking, and circuit breaking remain unimplemented. The earlier [OpenCode session](../results/experiment-03/shwapno/lwa-web-fresh-opencode-session.json) read a pre-generated Markdown file. A later [actual MCP pilot](../results/experiment-03/offline-agent-pilot-run-20261021/report.md) matched 15/20 frozen saved-capture answers, with exact-code, entity, omission, and timeout failures; without a matched baseline it cannot establish a causal accuracy or cost advantage. The [MCP mitigation design](lwa-web-mcp-mitigation-design.md) states the remaining acceptance checks.
