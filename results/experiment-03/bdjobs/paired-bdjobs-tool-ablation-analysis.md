# Site BD-CL02: Bdjobs.com — Controlled Playwright vs. Static Tool Ablation Audit

**Target URL:** `https://www.bdjobs.com`  
**Platform Architecture:** Angular Single-Page Application (SPA) with Server-Side Rendering (SSR) Skeleton, Client-Side Dynamic Hydration, and CDN Asset Pipelines (Bdjobs.com)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash) probing quantitative live job counters, animated typewriter input placeholders, in-image job fair banners, multi-frame GIF badges, tab selection states, and customer service affordances.  
**Contamination Check:** All four sessions executed in isolated environments with independent prompt contexts and zero cross-session memory.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID / Task ID | Retrieval Tooling | Wall-Clock Latency | Empirical Processing Strategy |
|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `task-1789` | Playwright browser evaluate + ImageMagick banner cropping | **208.0 s** (3.47 min) | Headless browser execution + dynamic typewriter sampling + selective banner cropping |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1793` | Playwright DOM snapshot + high-resolution fullpage visual analysis | **504.0 s** (8.40 min) | Visual screenshot examination + DOM attribute cross-referencing |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `task-1799` | `curl` static fetch + 82 Angular JavaScript chunk downloads + AST grep scripts | **283.0 s** (4.72 min) *(Crashed)* | **Cost & Token Limit Exhaustion**: Agent attempted reverse-engineering 82 Angular chunks until OpenRouter $2.00 hard limit was exceeded |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1829` | Static DOM inspection (`bd-cl02-dom.html`) + local raster asset inspection | **278.0 s** (4.63 min) | Direct static DOM parsing + localized raster graphic OCR reading |

---

## 2. Evaluation Against Researcher-Annotated Reference (20 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD-CL02-01** | **Live Jobs Counter** | `TEXT / METRIC` | 6,931 | **PASS** (6,931) | **PASS** (6,931) | **FAIL (Token Limit Crash)** | **PASS** (6,931) | Static parity / Cost crash |
| **BD-CL02-02** | **Vacancies Counter** | `TEXT / METRIC` | 28,916+ | **PASS** (28,916+) | **PASS** (28,916+) | **FAIL (Token Limit Crash)** | **PASS** (28,916+) | Static parity / Cost crash |
| **BD-CL02-03** | **Companies Counter** | `TEXT / METRIC` | 3,772 | **PASS** (3,772) | **PASS** (3,772) | **FAIL (Token Limit Crash)** | **PASS** (3,772) | Static parity / Cost crash |
| **BD-CL02-04** | **New Jobs Counter** | `TEXT / METRIC` | 759 | **PASS** (759) | **PASS** (759) | **FAIL (Token Limit Crash)** | **PASS** (759) | Static parity / Cost crash |
| **BD-CL02-05** | **Keyword Search Placeholder** | `DYNAMIC_INPUT` | `placeholder="Execut"` (Dynamic typewriter effect) | **PASS** (Captured rotation: Accounts, Web Dev, Execut) | **PASS** (Observed `Exe` in render, `Execut` in DOM) | **FAIL (Token Limit Crash)** | **PASS** (`Execut`) | **Dynamic Typewriter Cycle Gap** |
| **BD-CL02-06** | **Organization Dropdown Placeholder** | `UI_INPUT` | `Organization Type` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Static parity |
| **BD-CL02-07** | **Search Submit Button & Styling** | `BUTTON_UI` | `Search` with light-green background `bg-[#b8dbb8]` | **PASS** (Verbatim, `#b8dbb8`) | **PASS** (Verbatim, `#b8dbb8`) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim, `#b8dbb8`) | Static parity |
| **BD-CL02-08** | **Dhaka Quick Division Filter** | `TEXT / FILTER` | `Dhaka (4856)` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Static parity |
| **BD-CL02-09** | **Chattogram Quick Division Filter** | `TEXT / FILTER` | `Chattogram (561)` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Static parity |
| **BD-CL02-10** | **Barishal Quick Division Filter** | `TEXT / FILTER` | `Barishal (76)` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Static parity |
| **BD-CL02-11** | **Job Fair Banner Bangla Title** | `IN_IMAGE_GRAPHIC` | `জাতীয় যুবদিবস ২০২৬ উপলক্ষে জব ফেয়ার` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | **Trapped Raster Pixel Banner** |
| **BD-CL02-12** | **Job Fair Banner Red Date Badge** | `IN_IMAGE_GRAPHIC` | `০১ নভেম্বর` (01 November) | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | **Trapped Raster Pixel Badge** |
| **BD-CL02-13** | **Job Fair Organizing Authorities** | `IN_IMAGE_GRAPHIC` | `যুব উন্নয়ন অধিদপ্তর` / `যুব ও ক্রীড়া মন্ত্রণালয়` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | **Trapped Logo Pixel Typography** |
| **BD-CL02-14** | **Training Program Banner Title** | `IN_IMAGE_GRAPHIC` | `Winter School on Development in Practice 2026` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | **Trapped Raster Pixel Typography** |
| **BD-CL02-15** | **Training Program Application Deadline** | `IN_IMAGE_GRAPHIC` | `October 22` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | **Trapped Raster Pixel Typography** |
| **BD-CL02-16** | **Sidebar Badge 1 (Army-Banner.gif)** | `IN_IMAGE_GRAPHIC` | `Retired army person?` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Multi-frame GIF text extraction |
| **BD-CL02-17** | **Sidebar Badge 2 (video-cv.gif)** | `IN_IMAGE_GRAPHIC` | `Video CV click to upload` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Multi-frame GIF text extraction |
| **BD-CL02-18** | **Category vs Industry Active Tab** | `UI_STATE` | `Category` (active `bg-[#616161] text-white`) vs `Industry` (inactive) | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Interactive Tab Class State |
| **BD-CL02-19** | **Marketing/Sales Category Metric** | `TEXT / METRIC` | `Marketing/Sales (1273)` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Static parity |
| **BD-CL02-20** | **Customer Support Hotlines** | `TEXT / CONTACT` | `16479`, `09638666444`, `01897627858` | **PASS** (Verbatim) | **PASS** (Verbatim) | **FAIL (Token Limit Crash)** | **PASS** (Verbatim) | Contact Information Parity |

---

## 3. Major Scientific Discoveries from Bdjobs.com

### Finding 1: The Catastrophic Token & Cost Explosion of Static SPA Scraping
- In the static condition (Arm 3), OpenCode discovered that Bdjobs is an Angular SPA with SSR hydration. The initial HTML payload contained skeleton loaders while dynamic data was loaded from backend JSON APIs.
- Deprived of browser automation, the agent attempted to reverse engineer 82 separate Webpack/Angular JavaScript chunks (`chunk-*.js`) and trace client API bindings.
- Over 1,484 terminal interaction steps, the agent issued dozens of secondary `curl` commands, wrote custom Python AST search scripts, and examined Angular pipe definitions (`bengaliDigits`, `currency`, `timeAgo`).
- This compensatory feedback loop consumed all available context and exhausted the OpenRouter API key's financial limit (`$2.01 of $2.00 used`), terminating the session in a complete failure before any questions could be answered.
- **Significance**: Provides quantitative validation of the **Inverted Cost Curve** of modern web scraping. Static scraping on modern SPAs is not only less reliable, but exponentially more expensive in token usage and compute when LLM agents enter autonomous reverse-engineering loops.

### Finding 2: The Animated Typewriter Placeholder Temporal Gap (BD-CL02-05)
- The search input field (`input[name="txtSearch"]`) employs a client-side JavaScript typewriter animation cycling through suggested search keywords (e.g., "Accounts", "Web Developer", "Front-End...", "Executive...").
- In Playwright, OpenCode used `browser_evaluate` to sample the placeholder over 5 intervals (1.2s delay), capturing the rotating phrases. Antigravity observed `Exe` in the rendered screenshot and `Execut` in the captured DOM attribute.
- **Significance**: Highlights a temporal information gap where single-point DOM snapshots freeze intermediate typing state, whereas visual or dynamic agents can observe cyclic text transformations.

### Finding 3: In-Image Graphic Trapping in Classifieds & Employment Banners (BD-CL02-11 to BD-CL02-15)
- The top header banner (`1140X90.jpg`) contained critical event metadata regarding the National Youth Day Job Fair ("জাতীয় যুবদিবস ২০২৬ উপলক্ষে জব ফেয়ার", date "০১ নভেম্বর", and organizing ministries). In the DOM, the image tag rendered generic placeholder alt text: `<img alt="Top Default">`.
- Similarly, the Friendship Academy banner (`Friendship-Academy.jpg`) and sidebar badges (`Army-Banner.gif`, `video-cv.gif`) had completely empty `alt=""` attributes.
- In both Playwright and Static modalities, agents that performed visual raster inspection and targeted cropping successfully recovered 100% of the in-image Bengali and English typography, while DOM-only scrapers would fail completely.
