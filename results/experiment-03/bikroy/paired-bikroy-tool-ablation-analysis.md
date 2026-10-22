# Site BD-CL01: Bikroy.com — Controlled Playwright vs. Static Tool Ablation Audit

**Target URL:** `https://bikroy.com`  
**Platform Architecture:** Nuxt SSR with Client-Side Hydration and Dynamic Ad Card Grids (Saltside / Jiji Classifieds)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash) with visual anti-fraud watermark and unlabeled SVG flag stress tests.  
**Contamination Check:** All four sessions executed in isolated environments with independent prompt contexts and zero cross-session memory.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID | Retrieval Tooling | Input Tokens (Uncached) | Cache Read Tokens | Output Tokens (inc reasoning) | Total Processed Tokens | Billed / Equiv Cost | Wall-Clock Latency |
|---|---|---|---|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eac6d0793ffezG7Rn1sYguMprB` | `playwright_browser_navigate`, viewport snapshot, high-res visual crop & OCR | **52,637** | **610,048** | **3,206** (+13,339 reas) | **679,230** | **$0.079534** (OpenRouter) | **125.03 s** (2.08 min) |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `02a9725d-0603-4ed3-94d4-b6bafc65949e` | `call_mcp_tool` Playwright Chromium + high-res element inspect | **257,418** | **2,145,439** | **27,550** | **2,430,407** | **$0.067798** (Gemini Rate Card) | **384.00 s** (6.40 min) |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eac61541bffeEmwC3g54EeHw3g` | `curl` + bash ripgrep/regex scripts, parsed 208KB Nuxt SSR DOM chunks | **57,683** | **1,638,656** | **9,880** (+18,920 reas) | **1,725,139** | **$0.159137** (OpenRouter) | **183.12 s** (3.05 min) |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `1e63e313-8f01-4df1-8a94-ccaa96fa9ad1` | `curl` + 81 Python scripts, downloaded raster assets to `/tmp`, 8 `view_file` calls | **379,999** | **5,605,145** | **45,161** | **6,030,305** | **$0.147145** (Gemini Rate Card) | **856.00 s** (14.27 min) |

---

## 2. Evaluation Against Researcher-Annotated Reference (20 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD-CL01-01** | **Seller Watermark: Symphony Z42 Pro** | `IN_IMAGE_GRAPHIC` | `IFTEKHAR RAYAN` | **PASS** (Read via crop) | **PASS** (Read via crop) | **FAIL (Reported Not Found)** | **PASS** (Downloaded image + OCR) | **Gap 1 Confirmed**: Dropped in static Qwen |
| **BD-CL01-02** | **Seller Watermark: Vivo Y27s** | `IN_IMAGE_GRAPHIC` | `MD ABU RAYHAN` | **PASS** (Read via crop) | **PASS** (Read via crop) | **FAIL (Reported Not Found)** | **PASS** (Downloaded image + OCR) | **Gap 1 Confirmed**: Dropped in static Qwen |
| **BD-CL01-03** | **Seller Watermark: Nothing CMF Phone** | `IN_IMAGE_GRAPHIC` | `HASSAN` (or Nothing 3a `GANER DUNIYA`) | **PASS** (Found Nothing 3a variant) | **PASS** (Identified variant) | **FAIL (Reported Not Found)** | **PASS** (Retrieved listing image) | **Gap 1 Confirmed**: Dropped in static Qwen |
| **BD-CL01-04** | **Seller Watermark: Oppo 256 GB** | `IN_IMAGE_GRAPHIC` | `TM TAIOB` / `ROHIBUL ISLAM` | **PASS** (Read via crop) | **PASS** (Read via crop) | **FAIL (Reported Not Found)** | **PASS** (Retrieved listing image) | **Gap 1 Confirmed**: Dropped in static Qwen |
| **BD-CL01-05** | **Visual VIP Ad Crown Badge** | `IN_IMAGE_GRAPHIC` | Golden Crown icon (`ps-vip-icon.svg`), VIP | **PASS** (Golden crown, VIP) | **PASS** (Golden crown, VIP) | **PASS** (Found SVG alt "vip") | **PASS** (Golden crown, VIP) | Grounded across all setups |
| **BD-CL01-06** | Member Tenure Badge: TVS Stryker 125 | `TEXT / BADGE` | `5+ years on Bikroy` | **PASS** (Found in search) | **PASS** (Found in search) | **FAIL (Not on homepage)** | **PASS** (Retrieved advert page) | Preserved in search/advert |
| **BD-CL01-07** | Member Tenure Badge: Redmi Note 9 Pro Max | `TEXT / BADGE` | `3+ years on Bikroy` | **PASS** (3+ years) | **PASS** (3+ years) | **PASS** (3+ years) | **PASS** (3+ years) | Static parity |
| **BD-CL01-08** | Member Tenure Badge: Hunter ATV Quad Bike | `TEXT / BADGE` | `5+ years on Bikroy` | **PASS** (5+ years) | **PASS** (5+ years) | **PASS** (5+ years) | **PASS** (5+ years) | Static parity |
| **BD-CL01-09** | **Footer Sister Country Flag Icons** | `IN_IMAGE_GRAPHIC` | Nigeria, Kenya, Uganda, Tanzania, Ghana, Ethiopia... | **PASS** (All identified) | **PASS** (All identified) | **PASS** (Identified via domain URLs) | **PASS** (All 13 identified) | Flag icons grounded |
| **BD-CL01-10** | Category Metric: Phones & Tablets | `TEXT` | `88,617` (Live state) / Skeleton loader | **PASS** (Read hydrated count) | **PASS** (Skeleton detected) | **FAIL (Skeleton loader)** | **PASS** (Parsed Nuxt state) | **Dynamic hydration gap** |
| **BD-CL01-11** | Category Metric: Vehicles | `TEXT` | `31,247` (Live state) / Skeleton loader | **PASS** (Read hydrated count) | **PASS** (Skeleton detected) | **FAIL (Skeleton loader)** | **PASS** (Parsed Nuxt state) | **Dynamic hydration gap** |
| **BD-CL01-12** | Category Metric: Property | `TEXT` | `13,948` (Live state) / Skeleton loader | **PASS** (Read hydrated count) | **PASS** (Skeleton detected) | **FAIL (Skeleton loader)** | **PASS** (Parsed Nuxt state) | **Dynamic hydration gap** |
| **BD-CL01-13** | Category Metric: Electronics | `TEXT` | `58,719` (Live state) / Skeleton loader | **PASS** (Read hydrated count) | **PASS** (Skeleton detected) | **FAIL (Skeleton loader)** | **PASS** (Parsed Nuxt state) | **Dynamic hydration gap** |
| **BD-CL01-14** | Category Metric: Animals & Pets | `TEXT` | `15,523` (Live state) / Skeleton loader | **PASS** (Read hydrated count) | **PASS** (Skeleton detected) | **FAIL (Skeleton loader)** | **PASS** (Parsed Nuxt state) | **Dynamic hydration gap** |
| **BD-CL01-15** | Listing 1 Details: Itel S26 Ultra | `TEXT` | BDT 18,000 / Shariatpur, Zanjira | **PASS** (BDT 18,000, Zanjira) | **PASS** (BDT 18,000, Zanjira) | **PASS** (BDT 18,000, Zanjira) | **PASS** (BDT 12,500/18,000) | Static parity |
| **BD-CL01-16** | Listing 2 Details: Hunter ATV Quad Bike | `TEXT` | BDT 1,90,000 / Dhaka, Dhanmondi | **PASS** (BDT 1,90,000, Dhanmondi) | **PASS** (BDT 1,90,000, Dhanmondi) | **PASS** (BDT 1,90,000, Dhanmondi) | **PASS** (BDT 1,90,000, Dhanmondi) | Static parity |
| **BD-CL01-17** | Listing 3 Details: Honda Shine SP 2024 Black | `TEXT` | BDT 89,000 / Nilphamari, Nilphamari Sadar | **PASS** (BDT 89,000, Nilphamari) | **PASS** (BDT 89,000, Nilphamari) | **PASS** (BDT 89,000, Nilphamari) | **PASS** (BDT 89,000, Nilphamari) | Static parity |
| **BD-CL01-18** | Main Search Headline & Location Selector | `TEXT` | "What are you looking for?" / "All Bangladesh" | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-CL01-19** | Action Buttons | `TEXT` | "Post ad", "Trending" / "Niche Intelligence", "Apply for job" | **PASS** (All identified) | **PASS** (All identified) | **PASS** (Pills noted) | **PASS** (All identified) | Static parity |
| **BD-CL01-20** | Official Support Email | `TEXT` | `support@bikroy.com` | **PASS** (support@bikroy.com) | **PASS** (support@bikroy.com) | **PASS** (support@bikroy.com) | **PASS** (support@bikroy.com) | Static parity |

---

## 3. Major Scientific Discoveries from the Bikroy Benchmark

### Finding 1: Direct Confirmation of the Human-Agent In-Image Watermark Barrier
- On Bikroy.com, user-uploaded listing photos are automatically stamped with semi-transparent text: `"POSTED ON BIKROY <SELLER_NAME>"`.
- This information has **0% presence in the DOM or JSON-LD schema**.
- **Condition 1 (With Playwright)**: Both Qwen 3.8 and Gemini 3.8 successfully identified the seller watermarks by cropping listing elements and inspecting the image canvas.
- **Condition 2 (Without Playwright)**: OpenCode (Qwen 3.8) completely failed and reported `Not Found`, stating explicitly:
  > *"The 'POSTED ON BIKROY <SELLER_NAME>' text is rasterized inside the uploaded photo. Static requests return only the image bytes; with no OCR/visual tooling available, the exact name cannot be read."*
- Antigravity (Gemini 3.8) only extracted the watermarks by initiating an intensive compensatory loop: writing 81 Python scripts to download individual `.webp` image assets to `/tmp` and executing 8 `view_file` visual inspection steps over 14.27 minutes.

### Finding 2: Re-confirmation of the "Inverted Cost Paradox"
Ablating browser automation does not decrease API cost; it dramatically inflates it:
- **OpenCode / Qwen 3.8 27B**:
  - With Playwright: **679,230 tokens**, **$0.079534**, **125.03 s**.
  - Without Playwright: **1,725,139 tokens**, **$0.159137**, **183.12 s** (**+100.1% cost surge**).
- **Antigravity / Gemini 3.8 Flash**:
  - With Playwright: **2,430,407 tokens**, **$0.067798**, **384.00 s**.
  - Without Playwright: **6,030,305 tokens**, **$0.147145**, **856.00 s** (**+117.0% cost surge**, **2.2x latency surge**).

### Finding 3: Dynamic Skeleton Loaders in Nuxt SSR DOM
- In the static HTML shell delivered by SSR, the category advertisement counts on the left sidebar are returned as:
  `<div class="fw-skeleton-loader"></div>`.
- Without client-side hydration via browser JavaScript or deep payload reverse-engineering, static agents perceive category volumes as null or absent.
