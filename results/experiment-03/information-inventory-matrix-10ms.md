# Experiment 03 — Information Inventory Matrix: Site BD-ED01 (10 Minute School)

**Target URL:** `https://10minuteschool.com`  
**Platform:** 10 Minute School (Next.js SSR / Tailwind / CDN Asset Pipeline)  
**Domain Stratum:** EdTech, Video Learning & Academic Course Gateways (Bangladesh)  
**Visual Capture:** [`data/stage-4/screenshots/bd-ed01-fullpage.png`](../../data/stage-4/screenshots/bd-ed01-fullpage.png) (1280 × 9,779 px, SHA-256 `8578ef854d2ba3a5...`)  
**Raw Static DOM:** [`data/stage-4/raw/bd-ed01-dom.html`](../../data/stage-4/raw/bd-ed01-dom.html) (462.4 KB, SHA-256 `fc5d302c4c55b640...`)  
**Evaluation Scope:** 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode and Antigravity) probing in-image graphic text contradictions, Bengali numeral metrics, offline branch addresses, and educational portal affordances.

---

## 1. Researcher-Annotated Reference Inventory (20 Discrete Items)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw Static DOM? | Target Research Check |
|---|---|---|---|---|---|
| **BD-ED01-01** | **In-Image Hero Card 1 Graphic Text: `HSC 26` (Trophy Graphic)** | `IN_IMAGE_GRAPHIC` | Top hero category card 1 | **No (0% in DOM)** — Stamped in `hsc26_1790838009695.png` | In-image graphic text grounding |
| **BD-ED01-02** | **In-Image Hero Card 4 Contradiction: `SSC 27` (Diploma Icon)** | `IN_IMAGE_GRAPHIC` | Top hero category card 4 | **No (0% in DOM)** — Graphic says `SSC 27`, text below says `দশম শ্রেণি` | **Visual vs Text Contradiction** |
| **BD-ED01-03** | **In-Image Hero Card 5 Graphic Text: `CLASS 9` (Pouch Icon)** | `IN_IMAGE_GRAPHIC` | Top hero category card 5 | **No (0% in DOM)** — Graphic says `CLASS 9`, text below says `৯ম শ্রেণি` | Visual vs Text Contradiction |
| **BD-ED01-04** | **In-Image Hero Card 6 Graphic Text: `CLASS 6,7,8` (Backpack Icon)** | `IN_IMAGE_GRAPHIC` | Top hero category card 6 | **No (0% in DOM)** — Graphic says `CLASS 6,7,8`, text below says `৬ষ্ঠ, ৭ম, ৮ম শ্রেণি` | Visual vs Text Contradiction |
| **BD-ED01-05** | **In-Image Subject Bundle Gift Badge (Red Gift Box with Gold Ribbon 🎁)** | `IN_IMAGE_GRAPHIC` | Online batch pills (e.g. Science bundle) | Partial (DOM has image tag with empty text) | Visual icon affordance |
| **BD-ED01-06** | **Hero Navigation Action Button (`ফ্রি ক্লাস (HSC) ->`)** | `DYNAMIC / BUTTON` | Green pill below category cards | Yes (links to `/event/hsc-online-batch/`) | Primary conversion affordance |
| **BD-ED01-07** | **Offline Branch 1: Uttara English Centre Address & Floor** | `TEXT` | English Centre card 1 | Yes (`লিফট: ৮, হাউজ: ২, রোড: ৭, সেক্টর: ৩, উত্তরা`) | Physical entity grounding |
| **BD-ED01-08** | **Offline Branch 2: Panthapath English Centre Address & Floor** | `TEXT` | English Centre card 2 | Yes (`লিফট: ২, হাউজ: ১৪৭/ এ/ ২, গ্রীন রোড, পান্থপথ`) | Physical entity grounding |
| **BD-ED01-09** | **Offline Branch 3: Mirpur English Centre Landmark & Pillar** | `TEXT` | English Centre card 3 | Yes (`লিফট: ৭, প্লট: ১১৪, সেনপাড়া পর্বতা, মিরপুর- ১০ (পিলার: ২৫৬)`) | Physical landmark grounding |
| **BD-ED01-10** | **Offline Branch 4: Moghbazar English Centre Address & Floor** | `TEXT` | English Centre card 4 | Yes (`লিফট: ৩, প্লট: ২০৬, আউটার সার্কুলার রোড (ওয়ারলেস সার্কেল)`) | Physical entity grounding |
| **BD-ED01-11** | **Offline Branch 5: Chattogram English Centre Address & Floor** | `TEXT` | English Centre card 5 | Yes (`লিফট: ৪, প্লট: ১৫৩, কাপাসগোলা রোড, চকবাজার (অলি খাঁ মসজিদ)`) | Physical entity grounding |
| **BD-ED01-12** | **English Course Audience Tier 1: Kids' English (`For KG - Class 5`)** | `TEXT / BADGE` | English course card 1 | Yes (`For KG - Class 5`) | Educational audience scoping |
| **BD-ED01-13** | **English Course Audience Tier 2: Spoken English Junior (`For Class 6-10`)** | `TEXT / BADGE` | English course card 2 | Yes (`For Class 6-10`) | Educational audience scoping |
| **BD-ED01-14** | **Online Batch Delivery Metric: Weekly Live Classes (`10টি সাপ্তাহিক লাইভ ক্লাস`)** | `TEXT / METRIC` | Features grid, Card 1 | Yes (`10টি সাপ্তাহিক লাইভ ক্লাস`) | Operational metric |
| **BD-ED01-15** | **AI Doubt Solver Brand Name (`TenTen` / `SuperSolve`)** | `TEXT / BRAND` | Features grid, Card 6 | Yes (`TenTen`, `SuperSolve`) | Proprietary tool entity |
| **BD-ED01-16** | **Current Active Academic Student Count Statistic (`৩০+ হাজার`)** | `TEXT / METRIC` | Online batch subtitle | Yes (`৩০+ হাজার Academic স্টুডেন্ট`) | Scale metric |
| **BD-ED01-17** | **Mobile App Total Downloads Metric (reference version disputed)** | `TEXT / METRIC` | App download banner Card 1 | Saved raw DOM contains `৫,০০,০০০+` in embedded card data, not the previously listed `৪,৫৮,৫৪৩+`. Historical run timing is not aligned. | Engagement metric; exact value unresolved |
| **BD-ED01-18** | **Google Play Store Rating & Reviewer Count (`৪.৫+`, `৩,০০,০০০ শিক্ষার্থী`)** | `TEXT / METRIC` | App download banner Card 2 | Yes (`৪.৫+`, `প্রায় ৩,০০,০০০`) | Social proof metric |
| **BD-ED01-19** | **Featured Parent Testimonial (`পূর্ণিমা লস্কর`, মা, শিক্ষার্থী: পারমিতা লস্কর)** | `RENDERED_TEXT / TESTIMONIAL` | Testimonial carousel in saved visual crop | Exact Bengali name absent from saved raw DOM; visible in `scratch/visual_crops/testimonial2.png`. Whether a later rendered DOM exposes it is unverified. | Attributed quote grounding |
| **BD-ED01-20** | **Customer Support Hotline (`16910`, `+880 9610916910`, `support@10minuteschool.com`)** | `TEXT / CONTACT` | Footer support column | Yes (Hotline 16910, email support) | Official support channels |
