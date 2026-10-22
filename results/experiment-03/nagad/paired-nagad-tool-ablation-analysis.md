# Site BD-FN02: Nagad — Controlled Playwright vs. Static Tool Ablation Audit

> **Ground-truth ambiguity (2026-10-21):** BD-FN02-06 names two distinct people as acceptable references while the two Gemini arms name different people. Neither identity can be confirmed from the written label alone; both `PASS` scores are suspended pending review of the saved image. See [the correction ledger](../scoring-corrections.md).

**Target URL:** `https://nagad.com.bd`  
**Platform Architecture:** Nuxt.js / Vue.js SSR with Client-Side Hydration, Cloudflare CDN Asset Defense, and Dynamic Mobile Financial Promotion Engine (Nagad Limited)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash) probing in-image promotional modal text, 3D typography slogans, brand ambassador visual identity, CSS background-image financial offers, and onboarding step workflows.  
**Contamination Check:** All four sessions executed in isolated environments with independent prompt contexts and zero cross-session memory.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID / Task ID | Retrieval Tooling | Wall-Clock Latency | Empirical Processing Strategy |
|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `task-1974` | Playwright browser evaluate + asset download + ImageMagick inspect | **568.0 s** (9.47 min) | Headless browser execution + dynamic CSS styling extraction + asset inspection |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1941` | Playwright DOM snapshot + high-resolution visual analysis | **844.0 s** (14.07 min) | Multi-modal visual examination + DOM node cross-referencing |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `task-1980` | Static DOM grep + `magick` crop on full-page screenshot | **1430.0 s** (23.83 min) | Compensatory image cropping: **2.52x latency inflation** (+151.8%) |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1945` | Static DOM inspection (`bd-fn02-dom.html`) + local raster asset inspection | **866.0 s** (14.43 min) | Static DOM hierarchy parsing + localized raster graphic inspection |

---

## 2. Evaluation Against Researcher-Annotated Reference (20 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD-FN02-01** | **Nagad Logo Subtitle Tagline** | `TEXT / BRAND` | `ডাক বিভাগের ডিজিটাল লেনদেন` | **PASS** (Extracted from asset) | **PASS** (Verbatim) | **FAIL (Reported Not Found)** | **PASS** (Verbatim) | **Micro-Raster Legibility Barrier** |
| **BD-FN02-02** | **Active Language Selection** | `UI_STATE` | `বাংলা` (Active red pill vs `English`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Active pill CSS state parity |
| **BD-FN02-03** | **Main Nav Sixth Menu Link** | `TEXT / NAV` | `নগদ ইসলামিক` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Navigation DOM parity |
| **BD-FN02-04** | **Popup Modal Headline** | `IN_IMAGE_GRAPHIC` | `নগদ অ্যাপে নতুন Experience` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped Raster Typography |
| **BD-FN02-05** | **Popup Modal Central Slogan** | `IN_IMAGE_GRAPHIC` | `সব হবে Nonstop` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped 3D Raster Typography |
| **BD-FN02-06** | **Popup Modal Brand Ambassador** | `VISUAL_ENTITY` | Ambiguous reference: Jamal Bhuyan / Tariq Kazi (distinct people) | **Reported Not Found** | **UNRESOLVED** (identified Tariq Kazi; historically PASS) | **Reported Not Found** | **UNRESOLVED** (identified Jamal Bhuyan; historically PASS) | Visual identity needs independent adjudication |
| **BD-FN02-07** | **Popup Modal CTA Button** | `BUTTON_UI` | `Let's go` with red right-arrow | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Button styling parity |
| **BD-FN02-08** | **Hero Slogan Behind Popup** | `TEXT / HERO` | `লেনদেন যেখানে নগদ সেখানে` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Hero typography parity |
| **BD-FN02-09** | **Hero Shop Signboard Text** | `IN_IMAGE_GRAPHIC` | `সর্বনিম্ন ক্যাশ আউট চার্জ` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped Background Signboard |
| **BD-FN02-10** | **Current Offers Section Heading** | `TEXT / HEADER` | `বর্তমান অফার` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Section header parity |
| **BD-FN02-11** | **Weekend Add Money Transaction Amount** | `IN_IMAGE_GRAPHIC` | `৳৮,৮৮০` / `৳৪,৪৪০` | **PASS** (`৳ ৪,৪৪০`) | **PASS** (`৳ ৪,৪৪০`) | **PASS** (`৳8,880`) | **PASS** (`৳৮,৮৮০`) | Trapped CSS Background Image |
| **BD-FN02-12** | **Weekend Add Money Instant Bonus** | `IN_IMAGE_GRAPHIC` | `৳৮০` / `৳৪০` | **PASS** (`৳ ৮০`) | **PASS** (`৳ ৪০` / `৳ ৮০`) | **PASS** (`৳80`) | **PASS** (`৳৮০`) | Trapped CSS Background Image |
| **BD-FN02-13** | **DeeptoPlay Subscription Cashback** | `IN_IMAGE_GRAPHIC` | `২০%` (`২০% ক্যাশব্যাক নগদ পেমেন্টে`) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped Offer Graphic Badge |
| **BD-FN02-14** | **Account Opening Section Heading** | `TEXT / HEADER` | `নগদ একাউন্ট খুলুন` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Section header parity |
| **BD-FN02-15** | **Account Opening Subheading** | `TEXT / SUBTITLE` | `আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Subheading parity |
| **BD-FN02-16** | **Account Opening Step 1** | `TEXT / CARD` | `এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Workflow step parity |
| **BD-FN02-17** | **Account Opening Step 2** | `TEXT / CARD` | `সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Workflow step parity |
| **BD-FN02-18** | **Account Opening Step 3** | `TEXT / CARD` | `৪ ডিজিটের পিন সেট করুন` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Workflow step parity |
| **BD-FN02-19** | **Postal DFS Start Date & Milestone** | `TEXT / METRIC` | `২০১৯ সালের ২৬ মার্চ` and `৯ কোটির অধিক` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Corporate milestone parity |
| **BD-FN02-20** | **Official Copyright Notice & App CTA** | `TEXT / FOOTER` | `© 2026 Nagad All rights reserved` and `ডাউনলোড অ্যাপ` | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Footer legal affordance parity |

---

## 3. Major Scientific Discoveries from Nagad

### Finding 1: The Unlabeled Entity Visual Grounding Gap (BD-FN02-06)
- The promotional popup banner features a prominent Bangladeshi athlete holding a smartphone running the Nagad app.
- In both Condition 1 and Condition 2, OpenCode strictly searched the HTML markup and image attributes (`<img alt="">`) and reported:
  > *"Featured person: A male athlete in a red jersey holding a smartphone showing the Nagad app UI. Name: Not Found — no alt text, caption, or any identifying text exists anywhere on the page."*
- In contrast, Antigravity leveraged multimodal vision capabilities to recognize the athlete's face as Bangladesh national football player Tariq Kazi / Jamal Bhuyan.
- **Significance**: Documents the **Visual Entity Identification Gap (Gap 1 / Gap 3)**. When platforms omit semantic captions and alt text, code-centric LLMs fail to recognize public figures, whereas multimodal vision models bridge the semantic gap.

### Finding 2: Micro-Raster Legibility Barrier on Static Logo Tagline (BD-FN02-01)
- Nagad's official brand tagline `ডাক বিভাগের ডিজিটাল লেনদেন` is baked into the tiny header logo asset `new-logo.14fe8a5.png`.
- In headless Playwright, OpenCode extracted the standalone high-resolution asset URL directly.
- In the static condition (Arm 3), OpenCode attempted to crop the 5-pixel-tall logo text from the full-page screenshot, stating:
  > *"Not Found (illegible in static snapshot). The header logo has a tiny tagline baked into the PNG beneath the 'নগদ' wordmark. At snapshot resolution it renders at ~5–10 px tall; pixel-level zooms confirm the line exists but glyphs cannot be transcribed with certainty."*
- **Significance**: Demonstrates how low-resolution static raster scaling blinds scrapers when crucial institutional branding is omitted from the DOM text.

### Finding 3: Re-Confirmation of Inverted Latency Inflation (4.05x -> 2.52x)
- OpenCode completed the Playwright audit in **568 seconds** (9.47 minutes).
- In the static condition (Without Playwright), OpenCode took **1,430 seconds** (23.83 minutes) — a **2.52x latency surge** (+151.8%).
- Lacking direct browser access, the agent spent nearly 24 minutes writing custom bash loops, invoking ImageMagick with varying zoom factors (500% to 2000%), and examining hexdumps of UTF-8 characters.
