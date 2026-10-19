# Site BD-02: Chaldal Grocery Delivery — Controlled Playwright vs. Static Tool Ablation Audit

**Target URL:** `https://chaldal.com`  
**Platform Architecture:** React/Egg Single Page Application with Server-Pre-rendered Components  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash).  
**Contamination Check:** All four sessions were executed in fresh headless CLI contexts with zero cross-session memory, past prompt contamination, or access to pre-registered matrices.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID | Retrieval Tooling | Input Tokens (Uncached) | Cache Read Tokens | Output Tokens (inc reasoning) | Total Processed Tokens | Billed / Equiv Cost | Wall-Clock Latency |
|---|---|---|---|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eae7b0364ffejm3MA4RjCAiCZi` | `playwright_browser_navigate`, `evaluate`, `take_screenshot` (element crop + zoom) | **25,174** | **204,416** | **1,826** (+1,904 reas) | **233,320** | **$0.024469** (OpenRouter) | **99.3 s** |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `c5bb8b15-6928-4fdb-8ae0-c7af4391c7bb` | `call_mcp_tool` Playwright Chromium | **183,552** | **1,518,488** | **18,440** | **1,720,480** | **$0.047770** (Gemini Rate Card) | **313.0 s** |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eae729402ffeEw1pK729feMavx` | `curl`, `webfetch` + 6 Python scripts, XOR hex decoder | **26,574** | **319,872** | **4,615** (+3,175 reas) | **354,236** | **$0.039509** (OpenRouter) | **186.8 s** |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `8203b69c-f097-40de-815e-c9f5bdbbe015` | `curl` + 24 Python parsing scripts, XOR hex decoder | **183,810** | **1,259,321** | **16,034** | **1,459,165** | **$0.042208** (Gemini Rate Card) | **191.0 s** |

---

## 2. Evaluation Against Pre-Registered Ground Truth (22 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD2-01** | Platform Identity | `TEXT` | Chaldal / Chaldal Limited | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-02** | Main Service Heading | `TEXT` | Grocery Delivered at your Doorstep | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-03** | Default Delivery Location | `DYNAMIC` | Dhaka | **Yes** | **Yes** | **Yes** | **Yes** | Embedded in state JSON |
| **BD2-04** | Search Input Placeholder | `DYNAMIC` | Search for products (e.g. eggs, milk, potato) | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-05** | Value Proposition 1: Catalog | `TEXT` | +15000 products to shop from | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-06** | Value Proposition 2: Payment | `TEXT` | Pay after receiving products | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-07** | Value Proposition 3: Delivery SLA | `TEXT` | Get your delivery within 1 hour | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-08** | Value Proposition 4: Savings | `TEXT` | Get offers that Save Money | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-09** | App Promotion Discount | `TEXT` | 5% off on first order | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-10** | Scale Metric: Warehouses | `TEXT` | 26 warehouses nationwide | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-11** | Scale Metric: Delivered Orders | `TEXT` | 5 million orders | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-12** | Scale Metric: Families Served | `TEXT` | 100,000 families | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-13** | Scale Metric: Customer Savings | `TEXT` | 340 million Taka | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-14** | Operating Cities Coverage | `TEXT` | Dhaka, Chattogram, Jashore | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-15** | Delivery Fee: Orders Below 400 | `TEXT / TABLE` | Dhaka: 59, Chattogram: 59, Jashore: 29 | **Yes** | **Yes** | **Yes** | **Yes** | High fidelity ASCII table parsing |
| **BD2-16** | Delivery Fee: Orders Above 400 | `TEXT / TABLE` | Dhaka: 49, Chattogram: 49, Jashore: 19 | **Yes** | **Yes** | **Yes** | **Yes** | High fidelity ASCII table parsing |
| **BD2-17** | **Perishable Goods Return Limit** | `EXPLICIT_NEGATIVE` | **1 (one) day for milk, fruits, vegetables** | **Yes** | **Yes** | **Yes** | **Yes** | **RQ4 preserved in collapsed DOM** |
| **BD2-18** | Standard Packaged Return Window | `TEXT` | 7 (seven) days unopened/unspoilt | **Yes** | **Yes** | **Yes** | **Yes** | Collapsed DOM accessible |
| **BD2-19** | Daily Operating Hours | `TEXT` | 7.30 am to 11 pm every day | **Yes** | **Yes** | **Yes** | **Yes** | Collapsed DOM accessible |
| **BD2-20** | **Visual Partner Brand Logos** | `IN_IMAGE_GRAPHIC` | **Pran, Reckitt, Nestle, Unilever, Marico, Godrej, Coca-Cola, MGI** | **Yes (100% exact: identifies MGI via visual crop)** | **Partial (Reports Fresh from filename `fresh.png`)** | **Partial (Reports Fresh from filename `fresh.png`)** | **Partial (Reports Fresh from filename `fresh.png`)** | **Decisive In-Image Grounding Barrier Confirmed** |
| **BD2-21** | Customer Service Hotline | `TEXT` | 16710 | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD2-22** | **Customer Support Email** | `DYNAMIC` | **support@chaldal.com** | **Yes** (Direct DOM extract) | **Yes** (Direct DOM extract) | **Yes** (Decoded Cloudflare XOR hex) | **Yes** (Decoded Cloudflare XOR hex) | Dynamic obfuscation overcome |

---

## 3. Key Empirical Findings from the Chaldal Tool Ablation

### Finding 1: The Visual In-Image Grounding Barrier (Item BD2-20)
- **The Ground Truth Grounding Conflict**:
  Under the section *"Popular on Chaldal"*, exactly eight partner brand logos are displayed. In the DOM, each logo is rendered as a bare `<img src="...">` tag without any `alt` attribute or text node.
  Crucially, the 8th logo asset is named `fresh.png` on the server (`.../LandingPage/images/fresh.png`), but the graphical artwork rendered on screen is the **MGI (Meghna Group of Industries)** logo.
- **Model Divergence**:
  - **OpenCode With Playwright**: Successfully detected that the brand logos lacked text descriptors. It autonomously issued a `playwright_browser_take_screenshot` targeting the logo container, flagged that the 8th logo had distinct graphic text, executed a zoomed-in device-scale screenshot (`/tmp/opencode/ngi-logo.png`), visually grounded the glyphs, and correctly reported:
    > *"MGI (tagline: 'Meghna Group of Industries'; asset filename is fresh.png, logo text reads 'Mgi')"*.
  - **All Other Conditions (Antigravity With/Without Playwright, OpenCode Static)**:
    Fell back to regex-parsing the image URLs and reported the 8th brand as **Fresh**.
  - **Theoretical Implication**: This is the first empirical observation in our study where a headless browser agent autonomously used localized multi-scale visual cropping to override erroneous DOM asset naming.

### Finding 2: Inverted Tool Ablation Economics (The "Compensatory Scripting Loop")
- In our Shohoz trial, disabling Playwright halved OpenCode's cost ($0.0119 to $0.0058) because the task completed in a single fast static request.
- In Chaldal, disabling Playwright **increased OpenCode's billed cost by 61.5% ($0.0245 to $0.0395) and nearly doubled latency from 99.3 s to 186.8 s**.
- **Root Cause**: Chaldal's static HTML is 1.8 MB and contains React serialized state and Cloudflare protections. Without Playwright's native DOM inspection, OpenCode had to iteratively write and execute 6 custom Python scripts, search string offsets across 1.8 million characters, and write a manual XOR decoder to de-obfuscate Cloudflare's email cipher.
- **Agentic Law**: When pages exceed 1 MB and feature client-side protections, browser automation can actually be *cheaper* and *faster* than unguided static code-generation loops.

### Finding 3: Collapsed Accordion DOM Penetration (Items BD2-17 & BD2-18)
- In the visual interface, the FAQ questions for *"What is your policy on refunds?"* and *"What are your delivery hours?"* are collapsed behind expandable `+` toggle accordions. Only *"How much do deliveries cost?"* is open by default.
- Despite this visual occlusion, all four runs scored 100% on the negative perishable policy constraint (1-day perishable vs 7-day packaged return limit).
- **Reason**: Unlike lazy-loaded SPAs where collapsed content is fetched on click via GraphQL/REST, Chaldal server-renders the answer containers directly into the DOM tree with CSS hiding. Both browser accessibility trees and static regex were able to read the hidden rules.
