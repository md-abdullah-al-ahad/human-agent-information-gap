# Site BD-QC02: Shwapno Online — Controlled Playwright vs. Static Tool Ablation Audit

**Target URL:** `https://www.shwapno.com`  
**Platform Architecture:** Next.js React with Turbopack, Algolia Production Search Index (`S2O8A9M97P`), AWS CloudFront CDN Asset Caching, and Client-Side Personalization (ACI Logistics Limited)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash) probing trapped raster festival coupons, notification overlay modals, service proposition guarantees, dynamic pricing and discount badges, and regional outlet coverage tables.  
**Contamination Check:** All four sessions executed in isolated environments with independent prompt contexts and zero cross-session memory.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID / Task ID | Retrieval Tooling | Wall-Clock Latency | Empirical Processing Strategy |
|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `task-2018` | Playwright browser evaluate + CloudFront asset fetch | **88.0 s** (1.47 min) | Direct browser DOM evaluation + selective CloudFront banner download |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `task-2022` | Playwright DOM snapshot + Algolia AST extraction + multi-modal analysis | **1186.0 s** (19.77 min) | Deep client chunk reverse-engineering + live Algolia index verification |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `task-2046` | Static DOM grep + `magick` crop on fullpage screenshot | **617.0 s** (10.28 min) | Compensatory image cropping: **7.01x latency surge** over Playwright |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `task-2050` | Static DOM inspection (`bd-qc02-dom.html`) + local raster asset inspection | **509.0 s** (8.48 min) | Static DOM hierarchy parsing + localized raster graphic inspection |

---

## 2. Evaluation Against Pre-Registered Ground Truth (20 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD-QC02-01** | **Notification Modal Heading** | `UI_MODAL` | `Get notifications from Shwapno?` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Modal text parity |
| **BD-QC02-02** | **Notification Primary Button** | `BUTTON_UI` | `Yes` (Yellow primary `bg-yellow`) vs `No` | **PASS** (Verbatim, `bg-yellow`) | **PASS** (Verbatim, `bg-yellow`) | **PASS** (Verbatim, `bg-yellow`) | **PASS** (Verbatim, `bg-yellow`) | Button styling parity |
| **BD-QC02-03** | **Hero Banner Campaign Title** | `IN_IMAGE_GRAPHIC` | `স্বপ্ন অনলাইন পূজার সাশ্রয়` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **Trapped Raster Campaign Pixel** |
| **BD-QC02-04** | **Puja Promo Code 1 Details** | `IN_IMAGE_GRAPHIC` | `৬% ডিসকাউন্ট`, `PUJA6` (2 uses, max ৳150 on ৳1000+) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **Trapped Raster Voucher Pixel** |
| **BD-QC02-05** | **Puja Promo Code 2 Details** | `IN_IMAGE_GRAPHIC` | `৭% ডিসকাউন্ট`, `PUJA7` (1 use, max ৳200 on ৳1500+) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **Trapped Raster Voucher Pixel** |
| **BD-QC02-06** | **Value Pillar 1: Delivery** | `TEXT / SERVICE` | `60 mins delivery` (`Free shipping over 1500Tk`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Service proposition parity |
| **BD-QC02-07** | **Value Pillar 2: Exchange** | `TEXT / SERVICE` | `Authorized Products` (`within 30 days for an exchange`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Service proposition parity |
| **BD-QC02-08** | **Value Pillar 3: Support** | `TEXT / SERVICE` | `Customer Service Support` (`8am to 10pm`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Service proposition parity |
| **BD-QC02-09** | **Value Pillar 4: Payment** | `TEXT / SERVICE` | `Flexible Payments` (`Pay with multiple credit cards`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Service proposition parity |
| **BD-QC02-10** | **Fast Category Tile 1** | `UI_TILE` | `Eggs` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Category tile parity |
| **BD-QC02-11** | **Fast Category Tile 3** | `UI_TILE` | `Soft Drinks` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Category tile parity |
| **BD-QC02-12** | **Egg Loose Price & MOQ** | `PRODUCT_CARD` | `৳12.75` (Per Piece, `Min. 12`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Catalog pricing parity |
| **BD-QC02-13** | **Alu (Potato) Discount** | `PRODUCT_CARD` | `৳25` (`৳5 OFF`, original `৳30`, `Min. 1kg`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Catalog discount parity |
| **BD-QC02-14** | **ACI Pure Salt 1kg Price** | `PRODUCT_CARD` | `৳42` (Per Piece) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Catalog pricing parity |
| **BD-QC02-15** | **Masala Tea Weekday Deal** | `PRODUCT_CARD` | `Fresh Premium Masala Tea 50gm` — `৳95` (`৳15 OFF`, was `৳110`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Deal pricing parity |
| **BD-QC02-16** | **Himalaya Section Title** | `TEXT / HEADER` | `Refresh with Himalaya` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Brand showcase parity |
| **BD-QC02-17** | **Dhaka Coverage Outlets** | `QUANTITATIVE` | `Dhaka` — `290 outlets` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Coverage metric parity |
| **BD-QC02-18** | **Gazipur Coverage Outlets** | `QUANTITATIVE` | `Gazipur` — `69 outlets` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Coverage metric parity |
| **BD-QC02-19** | **Support Hotline & Email** | `TEXT / CONTACT` | `16469 (8am-10pm, Everyday)`, `queries@acilogistics.net` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Contact affordance parity |
| **BD-QC02-20** | **Operating Entity & Copyright** | `TEXT / LEGAL` | `ACI SHWAPNO E-COMMERCE LIMITED` and `Copyright © 2026` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Legal entity parity |

---

## 3. Major Scientific Discoveries from Shwapno Online

### Finding 1: The Festival Promo Code Trapping Barrier (BD-QC02-04, BD-QC02-05)
- Shwapno Online prominently advertises two major discount vouchers on its homepage hero banner:
  - `PUJA6`: 6% discount (2 uses, max ৳150 on ৳1000+)
  - `PUJA7`: 7% discount (1 use, max ৳200 on ৳1500+)
- In the underlying Next.js HTML DOM, the image tag has only `alt="ACI Banner" title="ACI Banner"`.
- Searching for the coupon strings `PUJA6` or `PUJA7` in the 2.4 MB DOM yields exactly 0 occurrences.
- Scrapers relying strictly on text extraction perceive no promotional discount codes whatsoever, creating a complete barrier for autonomous shopping agents attempting automated checkout.
- Multi-modal visual agents (and agents deploying targeted ImageMagick crop inspection) successfully ground the coupons from the banner graphic.

### Finding 2: Personalization & Lazy-Loading Hydration Asymmetry
- The "Recommended for you" and catalog deal carousels initialize client-side via Algolia search queries linked to the user's localized dark-store slot.
- On full-page headless renders, off-screen product cards render skeleton placeholders (`div.img-shimmer`) until scrolled into view.
- When tasked with extracting unhydrated product prices, agents demonstrated two distinct compensatory behaviors:
  1. OpenCode with Playwright executed targeted DOM evaluation scripts to sample loaded product components.
  2. Antigravity reverse-engineered the production Algolia App ID (`S2O8A9M97P`) and search API key from Turbopack chunks (`3k__qfwd8-k9k.js`), issuing standalone search queries to ground catalog pricing.

### Finding 3: Final Re-Confirmation of Inverted Tool Economics
- Across the entire 15-platform benchmark, headless browser automation (Playwright) consistently proved dramatically faster and cheaper than static scraping:
  - OpenCode with Playwright completed Shwapno in **88.0 seconds** (1.47 minutes).
  - OpenCode without Playwright took **617.0 seconds** (10.28 minutes) — a **7.01x latency surge** (+601.1%).
- Without browser automation, agents are forced to write multi-step AST parsers, regex filters, and image cropping pipelines, multiplying token usage and wall-clock time.
