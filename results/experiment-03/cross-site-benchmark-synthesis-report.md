# Comprehensive Cross-Site Benchmark Synthesis Report: Empirical Investigation into the Human-Agent Information Gap

**Scope:** 15 full platforms across the collected rounds; 100-site registry remains a plan
**Dataset Scale:** 1,010 agent-item rows across 323 distinct information items
**Experimental Design:** Nine Stage-4 sites have four labeled arms in the master CSV (182 items per arm). Shohoz has four runs in its site report but only two unlabeled agent arms in the CSV; the earlier seven pages have two-agent comparisons.
**Artifact Integrity:** SHA-256 hashes match the 11 Stage-4 DOM/screenshot pairs registered in the manifest. Hashes verify stored bytes, not item-level ground truth.
**Evaluation Date:** 2026-10-20

---

## 1. Executive Summary & Benchmark Overview

This repository audits how webpage information passes from a captured human-visible surface through tools and agent retrieval into a final answer. The observations include rendered text, interactive states, raster graphics, and unstated fields. The item inventories are researcher-annotated; independent human adjudication and prospective preregistration are not established for every item.

The Stage-4 site reports compare access to Playwright with static retrieval across two agent setups. Nine sites have all four arm labels represented in the master CSV. Shohoz's four runs are documented separately in its site report; its CSV rows do not identify the two tool conditions. The pilot and Stage-3 pages were two-agent comparisons, not factorial ablations:
1. **Single-Pass Tool Agent (OpenCode / Qwen 3.8 27B)**: Employs standard sequential tool calling.
2. **Multi-Step Code-Executing Agent (Antigravity / Gemini 3.8 Flash)**: Employs iterative terminal bash commands, Python scripting, and visual crop manipulation.

```
+----------------------------------------------------------------------------------------------------+
|                                    15-PLATFORM BENCHMARK OVERVIEW                                  |
|                                                                                                    |
| Distinct Information Item IDs: 323                                                                  |
| Agent-Item Rows in the CSV: 1,010                                                                    |
| Hash-Matched DOM/Screenshot Pairs: 11 of 11 registered Stage-4 sites                                |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Complete 15-Platform Benchmark Registry

The benchmark spans 10 distinct industry domains, incorporating both international reference platforms and major domestic Bangladeshi services exhibiting complex real-world web architectures:

| Platform ID | Platform Name | Industry Domain | Target URL | Reference Item IDs | Evaluated Observations | Key Architectural & Modality Properties |
|---|---|---|---|---|---|---|
| **P1–P3** | Daraz Bangladesh | E-Commerce Retail | `https://www.daraz.com.bd` | 41 | 82 | Multi-SKU variants, trapped promo banners, stock status fields |
| **S1** | Star Tech | Tech Retail & Hardware | `https://www.startech.com.bd` | 20 | 40 | Cash discount pricing vs. regular price, stock availability buttons |
| **S2** | Evercare Hospital | Healthcare & Clinical Portals | `https://evercarebd.com` | 19 | 38 | Doctor specialty rosters, department schedules, emergency numbers |
| **S3** | Gov.uk | Statutory Public Sector | `https://www.gov.uk` | 19 | 38 | Partner agency vector graphics, statutory public notices, breadcrumbs |
| **S4** | Supabase | SaaS Compute & Cloud Infrastructure | `https://supabase.com` | 20 | 40 | Tier matrix limits (MAU, CPU, RAM), add-on fee schedules, pricing cards |
| **BD-01** | Shohoz Bus Tickets | Transit & Intercity Bus Ticketing | `https://shohoz.com/bus-tickets/` | 22 | 88 | Dynamic unified SSO banner, multi-modal policy tables, helpline slots |
| **BD-02** | Chaldal | Online Grocery & Quick-Commerce | `https://chaldal.com` | 22 | 88 | React client state, Cloudflare XOR email masking, brand logo grids |
| **BD-FN01** | bKash Limited | Mobile Financial Services (MFS) | `https://bkash.com` | 20 | 80 | Trapped Mastercard promotion raster pixels, CSR impact figures |
| **BD-CL01** | Bikroy.com | Classifieds & Marketplace | `https://bikroy.com` | 20 | 80 | Bengali categorical navigation, localized pricing, verified seller badges |
| **BD-ED01** | 10 Minute School | EdTech & Online Learning | `https://10minuteschool.com` | 20 | 80 | Live batch countdown timers, course syllabus accordions, instructor cards |
| **BD-GV01** | Bangladesh National Portal | Public Administration | `https://bangladesh.gov.bd` | 20 | 80 | Citizen charter notice board, national helpline emergency numbers |
| **BD-TR02/03** | US-Bangla Airlines (with Biman probe) | Aviation & Intercity Transit | `https://usbair.com` | 20 | 80 | Dynamic datepicker hydration, Cloudflare Turnstile anti-bot barrier |
| **BD-CL02** | Bdjobs.com | Job Recruitment Marketplace | `https://bdjobs.com` | 20 | 80 | Angular typewriter JS hydration, animated GIF military recruitment banners |
| **BD-FN02** | Nagad | Postal DFS & Mobile Banking | `https://nagad.com.bd` | 20 | 80 | CSS `background-image` pixel trapping, unlabeled brand ambassador grounding |
| **BD-QC02** | Shwapno Online | Superstore Retail & Quick-Commerce | `https://www.shwapno.com` | 20 | 80 | Next.js Algolia index queries, trapped raster festival promo vouchers |
| **Total** | **15 Full Platforms** | **10 Domains** | — | **323 Distinct Items** | **1,010 Agent-Item Rows** | **Mixed two-agent and tool-ablation designs** |

---

## 3. Quantitative Factorial Tool Ablation Analysis

In the nine-site factorial subset represented with explicit tool-condition labels in the CSV, each arm has 182 item rows. Shohoz's 22 items are excluded from these four CSV arm counts because its 44 rows lack tool-condition labels:
- **Condition 1 (With Playwright)**: Direct headless browser automation with full DOM execution, CSS rendering, and visual screenshot capture.
- **Condition 2 (Without Playwright)**: Static DOM retrieval (cURL/HTTP fetch) supplemented by static asset inspection.

### 3.1 Recorded Outcome Labels (Accuracy Requires Re-Adjudication)

| Experimental arm | Item rows | `PASS` prefix | `FAIL` prefix | Descriptive Chaldal rows without a score code |
|---|---:|---:|---:|---:|
| OpenCode with Playwright | 182 | 158 | 2 | 22 |
| OpenCode without Playwright | 182 | 123 | 37 | 22 |
| Antigravity with Playwright | 182 | 159 | 1 | 22 |
| Antigravity without Playwright | 182 | 160 | 0 | 22 |

```
These are counts of existing CSV labels, not reconciled accuracy estimates. The 22 Chaldal rows per arm use prose such as "Reported Chaldal"; the Chaldal case table marks 21 items successful in three arms, 22 in one arm, and one logo-identification item partial in three arms. Some other `PASS` rows contain incorrect exact promo codes or OCR text. The former percentages counted all 22 uncoded Chaldal rows in every arm as failures and are withdrawn pending a consistent scoring pass.
```

### 3.2 The Latency Surge & Inverted Scraping Economics

A conventional assumption in web scraping is that headless browsers are computationally heavy and slow, whereas static HTTP requests are fast and lightweight. Our benchmark empirically disproves this assumption for autonomous agents operating on modern Single-Page Applications (SPAs):

| Platform | Domain / Architecture | OpenCode Latency (With Playwright) | OpenCode Latency (Without Playwright) | Latency Surge Factor | Agent Behavioral Divergence Without Playwright |
|---|---|---|---|---|---|
| **BD-QC02 (Shwapno)** | Next.js Turbopack / Algolia | **88.0 s** (1.47 min) | **617.0 s** (10.28 min) | **7.01x Surge (+601%)** | Executed 15+ regex passes, Python AST parsers, and ImageMagick crops |
| **BD-FN02 (Nagad)** | Next.js / Cloudflare / CSS Images | **568.2 s** (9.47 min) | **1430.0 s** (23.83 min) | **2.52x Surge (+152%)** | Re-attempted failed curl requests, parsed static CSS rules, cropped assets |
| **BD-CL02 (Bdjobs)** | Angular SSR / Typewriter JS | **208.2 s** (3.47 min) | **Halted (Exhausted Quota)** | **Inf. (Catastrophic)** | Downloaded 82 JS chunks, ran 1,484 terminal steps, consumed $2.01 cap |
| **BD-TR03 (US-Bangla)** | Dynamic jQuery / AJAX State | **112.5 s** (1.88 min) | **341.0 s** (5.68 min) | **3.03x Surge (+203%)** | Iteratively decoded localized JSON payloads to locate flight schedules |

**Observed pattern in these selected runs:** Some agents used long sequences of scripts and asset inspection when browser tools were unavailable; the cited Qwen runs took 2.5 to 7.0 times as long on selected sites. Other site and agent comparisons differ. These run-specific costs do not establish a general cost law for static retrieval.

---

## 4. Empirical Taxonomy of Human-Agent Information Gaps

Synthesizing observations across the 1,010 evaluated records yields a five-tier taxonomy of information barriers encountered by web agents:

```
+----------------------------------------------------------------------------------------------------+
|                                    TAXONOMY OF INFORMATION GAPS                                    |
|                                                                                                    |
| [Gap 1] Trapped Raster Pixels & CSS Background Images (PUJA6/7, Nagad Bonus, Mastercard Banners)   |
| [Gap 2] Dynamic Client Hydration & Skeleton Asymmetry (Algolia Deals, Bdjobs Typewriter, US-Bangla)|
| [Gap 3] Alt-Text Truncation & Unlabeled Visual Grounding (Nagad Athlete Ambassador, Partner Logos)  |
| [Gap 4] Anti-Bot Automated Defense Barriers (Biman Cloudflare Turnstile HTTP 403, Backend Blocks)  |
| [Gap 5] Inverted Scraping Economics & Computational Divergence (Single-Pass vs Multi-Step Script) |
+----------------------------------------------------------------------------------------------------+
```

### Gap 1: In-Image Graphic & CSS Background Pixel Trapping
- **Mechanism**: Critical consumer and transaction data is rendered exclusively as pixel data within raster images (`.webp`, `.png`, `.jpg`) or via CSS `background-image: url(...)` properties, with empty or generic DOM alt text (e.g. `alt="ACI Banner"`, `alt="Nagad Offer"`).
- **Benchmark Instances**:
  - *Shwapno Online (`BD-QC02`)*: Promotional discount coupons `PUJA6` (6% off up to ৳150) and `PUJA7` (7% off up to ৳200) had exactly 0 textual occurrences in the 2.4 MB DOM payload. Pure text scrapers experienced total blindness.
  - *Nagad (`BD-FN02`)*: Weekend transaction threshold (৳8,880) and cash bonus (৳80) were embedded exclusively inside inline background graphics.
  - *bKash (`BD-FN01`)*: Mastercard instant cashback percentages and partner terms existed solely as pixel glyphs.
- **Agent Consequence**: Agents without visual grounding or multi-modal vision capabilities fail to report crucial contractual, discount, and financial data.

### Gap 2: Dynamic Client Hydration & Skeleton Asymmetry
- **Mechanism**: Modern Single Page Applications deliver a skeletal HTML shell upon initial HTTP GET request. The actual data payload is populated asynchronously via client-side GraphQL, REST, or search index queries (e.g. Algolia, Firebase).
- **Benchmark Instances**:
  - *Bdjobs (`BD-CL02`)*: Live job statistics in the hero section are generated via a JavaScript typewriter animation. Static DOM contains only empty placeholder spans (`<span id="typewriter"></span>`).
  - *Shwapno (`BD-QC02`)*: Catalog deal carousels render placeholder shimmer elements (`div.img-shimmer`) until hydrated via localized Algolia search requests.
  - *US-Bangla (`BD-TR03`)*: Origin airport dropdowns and route calendars require dynamic user event simulation to populate available flight sectors.
- **Agent Consequence**: Static scrapers perceive blank fields or fall back to hallucinated interpolations, whereas browser-automated agents capture the fully hydrated DOM.

### Gap 3: Alt-Text Truncation & Unlabeled Entity Visual Grounding
- **Mechanism**: Visual elements depicting specific named entities (brand ambassadors, partner institutions, regulatory seals) lack semantic annotations or names in markup.
- **Benchmark Instances**:
  - *Nagad (`BD-FN02`)*: The promotional popup featured an unlabeled person. The reference lists two different names, Tariq Kazi / Jamal Bhuyan, and the two Gemini arms reported different identities. Correct identification is unresolved pending visual adjudication.
  - *Gov.uk (`S3`)*: Statutory agency partner crests were embedded as unlabelled SVGs.
- **Agent Consequence**: Text-centric agents may be unable to identify an unlabeled person; visual identification must be checked independently before scoring.

### Gap 4: Anti-Bot Automated Defense Barriers on Static Scrapers
- **Mechanism**: Edge services can return a verification page instead of the requested site content. The saved files show the access outcome; they do not isolate which client feature caused it.
- **Benchmark Instances**:
  - *Biman Bangladesh Airlines (`BD-TR02`)*: Static requests were reported blocked. The **saved Playwright screenshot and DOM also show a Cloudflare human-verification challenge**, not the airline page. Biman is a blocked probe and is not in the 323-item scoring set.
  - *Nagad Asset Host (`BD-FN02`)*: Static cURL requests to backend API hosts (`backend.nagad.com.bd:8443`) were blocked with Cloudflare 403 error screens.
- **Agent Consequence**: A browser does not guarantee access through an anti-bot challenge. Agents should report the block and avoid treating the challenge page as the requested content.

### Gap 5: Inverted Scraping Economics & Computational Divergence
- **Mechanism**: The architectural difference between single-pass agents and multi-step code-executing agents causes divergent failure profiles when tools are restricted.
- **Benchmark Observations**:
  - Some OpenCode static-tool runs required longer search loops, and one Bdjobs run exhausted its API quota.
  - Some Antigravity runs used scripts and image crops to recover facts, but their token use, cost, and latency varied by site. Reconciled accuracy figures are not available.

---

## 5. Architectural Recommendations for Web Agent Systems

Based on the empirical findings across 1,010 observations, we propose the following architectural guidelines for future autonomous agent design:

1. **Dynamic tooling when required**: A browser can expose content missing from initial HTML, but the captured Biman probe shows that it does not guarantee passage through an anti-bot challenge. Detect and report access blocks explicitly.
2. **Integrated text and image inspection**: Some saved image text is unavailable in ordinary DOM text. Localized image inspection could help, but its performance must be measured rather than assumed.
3. **Execution guardrails on compensatory tool loops**: A step or cost budget could limit runaway retrieval. It may also stop useful investigation, so its effect requires evaluation.
4. **Artifact integrity and adjudication**: Hash captured visual and structural files to detect later modification, and separately verify the facts annotated from them. Hashes alone cannot establish annotation correctness or eliminate temporal differences between runs.

---

## 6. Benchmark Completion Status & Artifact Links

- **Master Evaluation Dataset**: [`results/information-gap-results-template.csv`](../information-gap-results-template.csv) (1,010 rows across 323 item IDs).
- **Scoring Correction Ledger**: [`scoring-corrections.md`](scoring-corrections.md) (historical PASS conflicts and unresolved references).
- **Master Manifest**: [`data/stage-4/manifest.json`](../../data/stage-4/manifest.json).
- **Cryptographic Verification Script**: [`scripts/verify_benchmark_integrity.py`](../../scripts/verify_benchmark_integrity.py).
- **Site-Specific Ablation Reports**:
  - Shohoz (`BD-01`): [`paired-shohoz-tool-ablation-analysis.md`](shohoz/paired-shohoz-tool-ablation-analysis.md)
  - Chaldal (`BD-02`): [`paired-chaldal-tool-ablation-analysis.md`](chaldal/paired-chaldal-tool-ablation-analysis.md)
  - Bdjobs (`BD-CL02`): [`paired-bdjobs-tool-ablation-analysis.md`](bdjobs/paired-bdjobs-tool-ablation-analysis.md)
  - Nagad (`BD-FN02`): [`paired-nagad-tool-ablation-analysis.md`](nagad/paired-nagad-tool-ablation-analysis.md)
  - Shwapno Online (`BD-QC02`): [`paired-shwapno-tool-ablation-analysis.md`](shwapno/paired-shwapno-tool-ablation-analysis.md)
