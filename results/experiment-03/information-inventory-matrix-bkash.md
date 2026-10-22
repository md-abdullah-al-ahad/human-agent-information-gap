# Experiment 03 — Information Inventory Matrix: Site BD-FN01 (bKash Limited)

**Target URL:** `https://www.bkash.com`  
**Platform:** bKash Limited (Mobile Financial Services / Fintech)  
**Domain Stratum:** Banking, Fintech & Mobile Wallets (Bangladesh)  
**Visual Capture:** [`data/stage-4/screenshots/bd-fn01-fullpage.png`](../../data/stage-4/screenshots/bd-fn01-fullpage.png) (1280 × 6,980 px, SHA-256 `f55b9d46d447aede...`)  
**Raw Static DOM:** [`data/stage-4/raw/bd-fn01-dom.html`](../../data/stage-4/raw/bd-fn01-dom.html) (235.5 KB, SHA-256 `ff093bd734e2bad4...`)  
**Evaluation Scope:** 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode and Antigravity) with heavy 50%+ in-image visual graphic stress testing.

---

## 1. Researcher-Annotated Reference Inventory (20 Discrete Items)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw Static DOM? | Target Research Check |
|---|---|---|---|---|---|
| **BD-FN01-01** | **Hero Banner Question Header (`আপনি কি জানেন?`)** | `IN_IMAGE_GRAPHIC` | Top carousel left yellow half | **No (0% in DOM)** | **Trapped visual banner headline** |
| **BD-FN01-02** | **Hero Banner Feature 1: PIN Reset (`পিন রিসেট`)** | `IN_IMAGE_GRAPHIC` | Top carousel right pink half | **No (0% in DOM)** | **Trapped visual feature bullet** |
| **BD-FN01-03** | **Hero Banner Feature 2: Statement Download (`একাউন্টের স্টেটমেন্ট ডাউনলোড`)** | `IN_IMAGE_GRAPHIC` | Top carousel right pink half | **No (0% in DOM)** | **Trapped visual feature bullet** |
| **BD-FN01-04** | **Hero Banner Feature 3: Transaction Info (`লেনদেন নিশ্চিত ও তথ্য জানা`)** | `IN_IMAGE_GRAPHIC` | Top carousel right pink half | **No (0% in DOM)** | **Trapped visual feature bullet** |
| **BD-FN01-05** | **Hero Banner Feature 4: Complaint Submission (`সার্ভিস নিয়ে অভিযোগ জমা`)** | `IN_IMAGE_GRAPHIC` | Top carousel right pink half | **No (0% in DOM)** | **Trapped visual feature bullet** |
| **BD-FN01-06** | **Hero Banner Feature 5: Network Info Update (`মোবাইল নেটওয়ার্ক পরিবর্তনের তথ্য আপডেট`)** | `IN_IMAGE_GRAPHIC` | Top carousel right pink half | **No (0% in DOM)** | **Trapped visual feature bullet** |
| **BD-FN01-07** | **Phone Mockup Step 1: NID Photo (`আপনার NID এর ছবি তুলুন`)** | `IN_IMAGE_GRAPHIC` | App mockup screen under "দ্রুত ও নিরাপদ লেনদেন" | **No (0% in DOM)** | **Trapped mobile infographic step** |
| **BD-FN01-08** | **Phone Mockup Step 2: Information Entry (`প্রয়োজনীয় তথ্য দিন`)** | `IN_IMAGE_GRAPHIC` | App mockup screen under "দ্রুত ও নিরাপদ লেনদেন" | **No (0% in DOM)** | **Trapped mobile infographic step** |
| **BD-FN01-09** | **Phone Mockup Step 3: Face Photo (`নিজের চেহারার ছবি তুলুন`)** | `IN_IMAGE_GRAPHIC` | App mockup screen under "দ্রুত ও নিরাপদ লেনদেন" | **No (0% in DOM)** | **Trapped mobile infographic step** |
| **BD-FN01-10** | **Security & Compliance Certification Badges (`PCI DSS, ISO 27001, ISO 27701, ISO 9001`)** | `IN_IMAGE_GRAPHIC` | Footer security certifications | Partial (Bengali transliteration in alt) | **Visual compliance badge grounding** |
| **BD-FN01-11** | **Live Chat Greeting (`Welcome to bKash Customer Service` / `Good Morning!`)** | `DYNAMIC` | Floating customer service overlay | **No (0% in DOM)** | **Dynamic widget injection** |
| **BD-FN01-12** | **Live Chat Language Selection Options (`English` and `বাংলা`)** | `DYNAMIC` | Floating customer service overlay | **No (0% in DOM)** | **Dynamic widget injection** |
| **BD-FN01-13** | **Vehicle Toll Cashback Cap (`৳২৫০ পর্যন্ত ক্যাশব্যাক`)** | `TEXT` | Offer card 3 (বিকাশ-এ টোল দিলেই ক্যাশব্যাক) | Yes | Quantitative promotional ceiling |
| **BD-FN01-14** | Featured Campaign Offers (`পেমেন্ট মানেই বিকাশ`, `সিএক্সপ্রেস-এ বিকাশ-এর অফার`, `বিকাশ-এ টোল দিলেই ক্যাশব্যাক`) | `TEXT` | Offers section | Yes | Commercial campaign roster |
| **BD-FN01-15** | Press Milestones (বিশ্বসাহিত্য কেন্দ্র ১২ বছর, ট্রাস্ট ব্যাংক-বিকাশ চুক্তি, বিদ্যুৎ বিল মার্চেন্ট পয়েন্ট) | `TEXT` | "নতুন কী আছে বিকাশ এ" | Yes | Corporate news fidelity |
| **BD-FN01-16** | Core 4 Consumer Financial Services (`পেমেন্ট`, `মোবাইল রিচার্জ`, `সেন্ড মানি`, `ক্যাশ আউট`) | `TEXT` | "সব আর্থিক সল্যুশন এক প্ল্যাটফর্মে" | Yes | Primary product portfolio |
| **BD-FN01-17** | Extended Service Carousel (`বিকাশ বান্ডেল`, `অ্যাড মানি`, `পে বিল`) | `TEXT` | "বিকাশ-এর সার্ভিস সম্পর্কে আরো জানুন" | Yes | Secondary product portfolio |
| **BD-FN01-18** | Business Client Segments (`অনলাইন ব্যবসা`, `মার্চেন্ট`, `শিক্ষা প্রতিষ্ঠান`, `কর্পোরেট এবং এন্টারপ্রাইজ`, `মাইক্রোফাইন্যান্স`) | `TEXT` | "ব্যবসার জন্য বিকাশ" grid | Yes | B2B market segmentation |
| **BD-FN01-19** | Top Navigation Menu Categories (`ক্যাম্পেইন`, `সার্ভিসেস`, `বিজনেস`, `কাস্টমার সার্ভিস`, `ক্যারিয়ার`, `পরিচিতি`, `ব্লগ`, `স্টুডেন্ট`) | `TEXT` | Header navigation bar | Yes | Information architecture |
| **BD-FN01-20** | Entity Identity & Brand Purpose (`বিকাশ বাংলাদেশের মানুষকে মোবাইল ফোনের মাধ্যমে দ্রুত, নিরাপদে ও সহজে টাকা পাঠানো...`) | `TEXT` | Footer brand statement | Yes | Mission statement fidelity |
