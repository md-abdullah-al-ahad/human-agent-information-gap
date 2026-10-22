# Experiment 03 — Information Inventory Matrix: Site BD-02 (Chaldal Grocery Delivery)

**Target URL:** `https://chaldal.com`  
**Platform:** Chaldal (Chaldal Limited)  
**Domain Stratum:** Online Grocery & Daily Essentials Delivery (Bangladesh)  
**Visual Capture:** [`data/stage-4/screenshots/chaldal-fullpage.png`](../../data/stage-4/screenshots/chaldal-fullpage.png) (1208 × 5,635 px, SHA-256 `8425cd9920b57d9712ba69a29a2ce59a7e5289f97d718ee0f3d00df05d442988`)  
**Raw Static DOM:** [`data/stage-4/raw/chaldal-dom.html`](../../data/stage-4/raw/chaldal-dom.html) (1.8 MB, SHA-256 `07388b92389166834a7bb390ddee1b36a0ff1b8a057d9864ad4dbf8e3617649c`)  
**Evaluation Scope:** Paired Tool Ablation — Condition 1 (With Playwright / Headless Browser) vs. Condition 2 (Without Playwright / Static Scraper) across OpenCode and Antigravity.

---

## 1. Researcher-Annotated Reference Inventory (22 Discrete Items)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw Static DOM? | Target Research Check |
|---|---|---|---|---|---|
| **BD2-01** | Platform Identity (`Chaldal` / `Chaldal Limited`) | `TEXT` | Header logo & footer copyright | Yes | Entity identification |
| **BD2-02** | Main Service Heading (`Grocery Delivered at your Doorstep`) | `TEXT` | Hero section H1 | Yes | Service scope extraction |
| **BD2-03** | Default Delivery Location (`Dhaka`) | `DYNAMIC` | Top navigation bar location picker | Yes (in JSON state) | Geo-contextual anchoring |
| **BD2-04** | Search Input Placeholder (`Search for products (e.g. eggs, milk, potato)`) | `DYNAMIC` | Hero search input | Yes | Search affordance |
| **BD2-05** | Value Proposition 1: Catalog Size (`+15000 products to shop from`) | `TEXT` | Feature grid item 1 | Yes | Quantitative claim fidelity |
| **BD2-06** | Value Proposition 2: Payment Policy (`Pay after receiving products`) | `TEXT` | Feature grid item 2 | Yes (nested markup) | Commercial policy extraction |
| **BD2-07** | Value Proposition 3: Delivery Commitment (`Get your delivery within 1 hour`) | `TEXT` | Feature grid item 3 | Yes | Temporal SLA extraction |
| **BD2-08** | Value Proposition 4: Savings Guarantee (`Get offers that Save Money`) | `TEXT` | Feature grid item 4 | Yes | Marketing claim extraction |
| **BD2-09** | App Discount Offer (`Get 5% off on your first order through the Chaldal app`) | `TEXT` | App download banner | Yes | Promotional incentive fidelity |
| **BD2-10** | Scale Metric: Warehouses (`26 warehouses all over bangladesh`) | `TEXT` | Scale statistics grid card 1 | Yes | Operational capacity metric |
| **BD2-11** | Scale Metric: Delivered Orders (`5 million orders have been delivered`) | `TEXT` | Scale statistics grid card 2 | Yes | Operational volume metric |
| **BD2-12** | Scale Metric: Families Served (`100,000 families are being served`) | `TEXT` | Scale statistics grid card 3 | Yes | Demographic reach metric |
| **BD2-13** | Scale Metric: Customer Savings (`340 million Taka customer savings`) | `TEXT` | Scale statistics grid card 4 | Yes | Economic impact metric |
| **BD2-14** | Active Operating Cities (`Dhaka`, `Chattogram`, `Jashore`) | `TEXT` | Coverage pills & footer | Yes | Geographical logistics scope |
| **BD2-15** | Delivery Fee Schedule: Below 400 BDT (`Dhaka: 59 BDT`, `Chattogram: 59 BDT`, `Jashore: 29 BDT`) | `TEXT / TABLE` | FAQ ASCII delivery fee table | Yes (text table) | Structural tabular parsing |
| **BD2-16** | Delivery Fee Schedule: Above 400 BDT (`Dhaka: 49 BDT`, `Chattogram: 49 BDT`, `Jashore: 19 BDT`) | `TEXT / TABLE` | FAQ ASCII delivery fee table | Yes (text table) | Tiered pricing extraction |
| **BD2-17** | **Perishable Return Limit: Milk, Fruits & Veg (`1 (one) day return policy`)** | `EXPLICIT_NEGATIVE` | FAQ Accordion 3 (Policy on refunds) | Yes (collapsed in UI) | **Negative policy constraint (RQ4)** |
| **BD2-18** | Standard Packaged Goods Return Window (`7 (seven) days unopened/unspoilt`) | `TEXT` | FAQ Accordion 3 (Policy on refunds) | Yes (collapsed in UI) | General return window |
| **BD2-19** | Operating Delivery Hours (`7.30 am to 11 pm every day`) | `TEXT` | FAQ Accordion 2 (Delivery hours) | Yes (collapsed in UI) | Temporal operating constraint |
| **BD2-20** | **Visual Partner Brand Logos (`Pran, Reckitt, Nestle, Unilever, Marico, Godrej, Coca-Cola, MGI`)** | `IN_IMAGE_GRAPHIC` | Popular on Chaldal brand logo strip | **Partial** (No `alt` tags; MGI image file is `fresh.png`) | **In-image visual grounding failure probe** |
| **BD2-21** | Customer Service Hotline (`16710`) | `TEXT` | Footer customer support | Yes | Telephonic affordance |
| **BD2-22** | Customer Service Email (`support@chaldal.com`) | `DYNAMIC` | Footer customer support | **No** (Missing in static HTML, rendered dynamically) | **Dynamic hydration gap probe** |

---

## 2. Experimental Tool Ablation Protocol

We execute the identical audit prompt across four experimental arms:
1. **OpenCode With Playwright** (Qwen 3.8 27B + Playwright headless browser MCP).
2. **Antigravity With Playwright** (Gemini 3.8 Flash + native browser / dynamic tools).
3. **OpenCode Without Playwright** (Qwen 3.8 27B + static HTTP GET / scraper only).
4. **Antigravity Without Playwright** (Gemini 3.8 Flash + curl / static scripts only).

---

## 3. Metrics Tracked
- **Extraction Completeness**: 22 pre-registered items scored as Observed (1.0), Partial (0.5), or Hallucinated/Missing (0.0).
- **In-Image Graphic Accuracy**: Detection and attribution of partner brand logos (specifically MGI / Meghna Group vs `fresh.png`).
- **Tabular Parsing Accuracy**: Strict correctness of the 400 BDT delivery fee threshold across Dhaka, Chattogram, and Jashore.
- **Resource Consumption**: Input tokens, Output/Reasoning tokens, Total tokens, Latency (seconds), and Billed cost (USD).
