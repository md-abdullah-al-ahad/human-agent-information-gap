# Experiment 03 — Information Inventory Matrix: Site BD-CL01 (Bikroy.com)

**Target URL:** `https://bikroy.com`  
**Platform:** Bikroy.com (Saltside / Jiji Classifieds)  
**Domain Stratum:** Classifieds, C2C & Used Goods Marketplace (Bangladesh)  
**Visual Capture:** [`data/stage-4/screenshots/bd-cl01-fullpage.png`](../../data/stage-4/screenshots/bd-cl01-fullpage.png) (1280 × 4,361 px, SHA-256 `74da1a8cf031ed10...`)  
**Raw Static DOM:** [`data/stage-4/raw/bd-cl01-dom.html`](../../data/stage-4/raw/bd-cl01-dom.html) (221.2 KB, SHA-256 `e42d25e2d3cd7c59...`)  
**Evaluation Scope:** 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode and Antigravity) with a heavy visual emphasis on in-image seller watermarks, visual VIP crown badges, and unlabeled flag icons.

---

## 1. Researcher-Annotated Reference Inventory (20 Discrete Items)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw Static DOM? | Target Research Check |
|---|---|---|---|---|---|
| **BD-CL01-01** | **In-Image Seller Watermark 1: Symphony Z42 Pro (`POSTED ON BIKROY IFTEKHAR RAYHAN`)** | `IN_IMAGE_GRAPHIC` | Stamped across the product photograph | **No (0% in DOM)** | **Trapped in-photo seller watermark** |
| **BD-CL01-02** | **In-Image Seller Watermark 2: Vivo Y27s (`POSTED ON BIKROY MD ABU RAYHAN`)** | `IN_IMAGE_GRAPHIC` | Stamped across the product photograph | **No (0% in DOM)** | **Trapped in-photo seller watermark** |
| **BD-CL01-03** | **In-Image Seller Watermark 3: Nothing CMF Phone 2 Pro (`POSTED ON BIKROY MASUDER`)** | `IN_IMAGE_GRAPHIC` | Stamped across the product photograph | **No (0% in DOM)** | **Trapped in-photo seller watermark** |
| **BD-CL01-04** | **In-Image Seller Watermark 4: Oppo 256 GB (`POSTED ON BIKROY MD ABU RAYHAN`)** | `IN_IMAGE_GRAPHIC` | Stamped across the product photograph | **No (0% in DOM)** | **Trapped in-photo seller watermark** |
| **BD-CL01-05** | **Visual VIP Ad Crown Badge (Golden Crown icon on New Xiaomi Civi 1S & Note 9 Pro Max)** | `IN_IMAGE_GRAPHIC` | Bottom right corner of card | Partial (Image alt is `vip`, icon is SVG golden crown) | **Visual icon grounding** |
| **BD-CL01-06** | Member Tenure Badge: TVS Stryker 125 (`5+ YEARS ON BIKROY`) | `TEXT / BADGE` | Overlay pill on top right of image | Yes (in DOM `5+ years on Bikroy`) | Visual vs DOM attribute parity |
| **BD-CL01-07** | Member Tenure Badge: Xiaomi Redmi Note 9 Pro Max (`3+ YEARS ON BIKROY`) | `TEXT / BADGE` | Overlay pill on top right of image | Yes (in DOM `3+ years on Bikroy`) | Visual vs DOM attribute parity |
| **BD-CL01-08** | Member Tenure Badge: Hunter ATV Quad Bike (`5+ YEARS ON BIKROY`) | `TEXT / BADGE` | Overlay pill on top right of image | Yes (in DOM `5+ years on Bikroy`) | Visual vs DOM attribute parity |
| **BD-CL01-09** | **Footer Sister Country Flag Icons (Circular flag icons e.g. Nigeria, Kenya, Ghana, Uganda, Sri Lanka)** | `IN_IMAGE_GRAPHIC` | Bottom footer sister sites | **No text in DOM** (Anchor tags have empty text nodes) | **Unlabeled visual flag grounding** |
| **BD-CL01-10** | Category Metric: Phones & Tablets Total Ads (`88,835 ads`) | `TEXT` | Left sidebar category list | Yes | Quantitative category metric |
| **BD-CL01-11** | Category Metric: Vehicles Total Ads (`31,108 ads`) | `TEXT` | Left sidebar category list | Yes | Quantitative category metric |
| **BD-CL01-12** | Category Metric: Property Total Ads (`13,985 ads`) | `TEXT` | Left sidebar category list | Yes | Quantitative category metric |
| **BD-CL01-13** | Category Metric: Electronics Total Ads (`58,865 ads`) | `TEXT` | Left sidebar category list | Yes | Quantitative category metric |
| **BD-CL01-14** | Category Metric: Animals & Pets Total Ads (`15,523 ads`) | `TEXT` | Left sidebar category list | Yes | Quantitative category metric |
| **BD-CL01-15** | Listing 1 Details: Itel S26 Ultra 256 GB Blue (`BDT 18,000`, `Shariatpur, Zanjira`, `Used`) | `TEXT` | Trending ads card 1 | Yes | C2C listing metadata extraction |
| **BD-CL01-16** | Listing 2 Details: New Motorcycle 2026 Yellow ATV (`BDT 1,90,000`, `Dhaka, Dhanmondi`, `Brand New`) | `TEXT` | Trending ads card 16 | Yes | C2C listing metadata extraction |
| **BD-CL01-17** | Listing 3 Details: Honda Shine SP 2024 Black (`BDT 89,000`, `Nilphamari, Nilphamari Sadar`, `Local Used`) | `TEXT` | Trending ads card 10 | Yes | C2C listing metadata extraction |
| **BD-CL01-18** | Main Search Headline (`What are you looking for?`) & Location Selector (`All Bangladesh`) | `TEXT` | Hero search area | Yes | Search affordance |
| **BD-CL01-19** | Action Buttons (`Niche Intelligence` and `Apply for job`) | `TEXT` | Hero pills below search | Yes | Navigation affordance |
| **BD-CL01-20** | Official Customer Support Contact Email (`support@bikroy.com`) | `TEXT` | Footer support column | Yes | Direct contact channel |
