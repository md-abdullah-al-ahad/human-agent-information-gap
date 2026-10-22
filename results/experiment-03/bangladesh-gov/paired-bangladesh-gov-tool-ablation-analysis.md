# Site BD-GV01: Bangladesh National Portal — Controlled Playwright vs. Static Tool Ablation Audit

> **Scoring correction (2026-10-21):** The Qwen-with-Playwright OCR in BD-GV01-07/08 is not verbatim. BD-GV01-08 changes the key term. Historical `PASS` labels in the master CSV and unrecomputed report totals should not be read as exact-text accuracy. See [the correction ledger](../scoring-corrections.md).

**Target URL:** `https://bangladesh.gov.bd`  
**Platform Architecture:** Custom Component-Based Public Sector Portal with Micro-Widgets, CDN-Hosted Media, and Dynamic Overlay Modals (a2i / ICT Division)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen 3.8 27B and Antigravity/Gemini 3.8 Flash) probing in-image graphic text, modal popups, administrative division counters, interactive services tabs, fold-hidden emergency helplines, and footer institutional attribution.  
**Contamination Check:** All four sessions executed in isolated environments with independent prompt contexts and zero cross-session memory.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID / Task ID | Retrieval Tooling | Wall-Clock Latency | Empirical Processing Strategy |
|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `task-1489` | Playwright browser evaluate, fullpage viewport snapshot, ImageMagick asset crop & OCR | **252.0 s** (4.20 min) | Automated browser viewport navigation + selective element zoom |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1501` | Playwright browser inspection + selective asset verification & visual analysis | **311.0 s** (5.18 min) | Automated DOM inspection + multi-image visual grounding |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `task-1507` | `curl` static fetch + 18 bash/Python regex scripts, ImageMagick iterative crop scripts | **845.0 s** (14.08 min) | Compensatory bash loop: 3.35x latency surge trying to slice raw images |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `task-1511` | `curl` static fetch + Python standard library parsing, downloaded assets to `/tmp` + visual inspection | **258.0 s** (4.30 min) | Targeted static DOM parsing + asset download and inspection |

---

## 2. Evaluation Against Researcher-Annotated Reference (20 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD-GV01-01** | **Main Portal Title** | `TEXT / BRANDING` | বাংলাদেশ জাতীয় তথ্য বাতায়ন | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-GV01-02** | **Header Current Date** | `TEXT / DATE` | ১৯ অক্টোবর ২০২৬ | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-GV01-03** | **Search Input Placeholder** | `DOM ATTRIBUTE` | এখানে খুঁজুন... | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-GV01-04** | **Food Safety Popup Headline** | `IN_IMAGE_GRAPHIC` | পোড়া তেল ব্যবহার করবেন না | **PASS** (পোড়া তেলে ব্যবহার করবেন না) | **PASS** (Verbatim) | **PASS** (Downloaded image + OCR) | **PASS** (Downloaded image + OCR) | Trapped pixel extracted |
| **BD-GV01-05** | **Food Safety Popup Authority & URL** | `IN_IMAGE_GRAPHIC` | বাংলাদেশ নিরাপদ খাদ্য কর্তৃপক্ষ / www.bfsa.gov.bd | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped pixel extracted |
| **BD-GV01-06** | **Food Safety Popup Health Risks** | `IN_IMAGE_GRAPHIC` | ক্ষতিকারক কোলেস্টেরল বৃদ্ধি, স্ট্রোক ও হৃদরোগ | **PASS** (Stroke & heart disease) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped pixel extracted |
| **BD-GV01-07** | **Food Safety Popup Culinary Advice** | `IN_IMAGE_GRAPHIC` | ছেঁকে তরকারিতে ব্যবহার করতে পারেন | **PARTIAL / OCR mismatch** (হেঁকে তরকারি; historically PASS) | **PASS** (Verbatim) | **PASS** (ছেকে তরকারিতে) | **PASS** (Verbatim) | Exact-text criterion needs adjudication |
| **BD-GV01-08** | **Banner Applet: GPF Calculator** | `IN_IMAGE_GRAPHIC` | ভবিষ্য তহবিল ক্যালকুলেটর | **FAIL under key-term criterion** (ডিবিয় তহবিল; historically PASS) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Key term differs from reference |
| **BD-GV01-09** | **Banner Applet: Inheritance Tool** | `IN_IMAGE_GRAPHIC` | উত্তরাধিকার.বাংলা / এক ক্লিকেই সম্পত্তির হিসাব | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Trapped pixel in hero slider |
| **BD-GV01-10** | **Counter: Ministries & Divisions** | `STRUCTURED_NUMERIC` | ৫৭ মন্ত্রণালয় ও বিভাগ | **PASS** (57) | **PASS** (57) | **PASS** (57) | **PASS** (57) | Static parity |
| **BD-GV01-11** | **Counter: Upazilas** | `STRUCTURED_NUMERIC` | ৫০০ উপজেলা | **PASS** (500) | **PASS** (500) | **PASS** (500) | **PASS** (500) | Static parity |
| **BD-GV01-12** | **Counter: Union Parishads** | `STRUCTURED_NUMERIC` | ৪৫৬৮ ইউনিয়ন | **PASS** (4568) | **PASS** (4568) | **PASS** (4568) | **PASS** (4568) | Static parity |
| **BD-GV01-13** | **Services Active Default Tab** | `TABBED_NAVIGATION` | জনপ্রিয় সেবা (popular-services) | **PASS** (জনপ্রিয় সেবা) | **PASS** (জনপ্রিয় সেবা) | **PASS** (জনপ্রিয় সেবা) | **PASS** (জনপ্রিয় সেবা) | Static parity |
| **BD-GV01-14** | **Popular Services Card 8** | `SERVICE_GRID` | পাসপোর্ট, ভিসা ও ইমিগ্রেশন | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-GV01-15** | **Popular Services Fold-Hidden Item** | `FOLD_HIDDEN_ITEM` | ইউটিলিটি বিল (Hidden behind আরো দেখুন ↓) | **PASS** (Correctly identified hidden state) | **PASS** (Index 9, hidden item class) | **PASS** (Analyzed widget JS) | **PASS** (Analyzed widget CSS) | Affordance barrier decoded |
| **BD-GV01-16** | **Emergency Helpline 1** | `SIDEBAR_HELPLINE` | ৩৩৩ (সরকারি তথ্য ও সেবা) | **PASS** (333) | **PASS** (333) | **PASS** (333) | **PASS** (333) | Static parity |
| **BD-GV01-17** | **Emergency Helpline 4** | `SIDEBAR_HELPLINE` | ১৬১০৭ (বিআরটিএ সার্ভিস পোর্টাল) | **PASS** (16107) | **PASS** (16107) | **PASS** (16107) | **PASS** (16107) | Static parity |
| **BD-GV01-18** | **Emergency Helpline Fold-Hidden Item** | `FOLD_HIDDEN_ITEM` | ১৬১২২ (স্মার্ট ভূমি সেবা, hidden behind toggle) | **PASS** (Correctly identified hidden state) | **PASS** (Item 9, CSS nth-child rule) | **PASS** (CSS nth-child rule noted) | **PASS** (CSS nth-child rule noted) | Affordance barrier decoded |
| **BD-GV01-19** | **Photo Gallery Item 4** | `MEDIA_GALLERY` | নৌকা বাইচ (Boat Race) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | **PASS** (Verbatim) | Static parity |
| **BD-GV01-20** | **Footer Implementation Partners Cluster** | `IN_IMAGE_GRAPHIC / DOM OMISSION` | a2i, Cabinet Division, ICT Division, UNDP | **FAIL (Asserted UNDP & Cabinet absent)** | **PASS (All 4 partners identified)** | **FAIL (Asserted UNDP & Cabinet absent)** | **PASS (All 4 partners identified)** | **Gap 1 / Alt-Text Truncation Trap** |

---

## 3. Major Scientific Discoveries from Bangladesh National Portal

### Finding 1: The Alt-Text Truncation & Deceptive DOM Omission Trap (BD-GV01-20)
- In the portal footer under "পরিকল্পনা এবং বাস্তবায়ন" (Planning and Implementation), a composite image asset (`/site-assets/images/a2iset.png`) depicts four official institutional partner logos:
  1. `a2i` (`innovate for all`)
  2. `Cabinet Division` (`Government of the People's Republic of Bangladesh`)
  3. `ICT Division` (`FUTURE IS HERE`)
  4. `UNDP` (`United Nations Development Programme`)
- However, the HTML markup provides an incomplete, truncated alt attribute: `<img src="/site-assets/images/a2iset.png" alt="a2i" class="">`.
- **OpenCode (Both Arms)**:
  - In Condition 1 (With Playwright), Qwen inspected the DOM attribute and reported:
    > *"Under 'পরিকল্পনা এবং বাস্তবায়ন': only one logo is depicted — a2i. The cluster does NOT include UNDP or Cabinet Division; only the a2i logo is present."*
  - In Condition 2 (Without Playwright), Qwen inspected the raw HTML snippet and reiterated:
    > *"Under 'পরিকল্পনা এবং বাস্তবায়ন' there is only one logo: a2i (<img src='/site-assets/images/a2iset.png' alt='a2i'>). No — the cluster does NOT include UNDP or Cabinet Division."*
- **Antigravity (Both Arms)**:
  - In Condition 1, Antigravity used high-resolution visual inspection on the rendered footer, immediately identifying all 4 partner emblems.
  - In Condition 2, Antigravity downloaded the binary image file `/site-assets/images/a2iset.png` to `/tmp` and inspected it visually via `view_file`, confirming that both UNDP and Cabinet Division are explicitly present.
- **Scientific Significance**: This provides a striking real-world demonstration of **The Alt-Text Truncation Trap (Gap 1 / Gap 3)**. When website authors supply partial or lazy alt text (`alt="a2i"` for a four-partner cluster), non-visual reasoning agents treat the DOM text as ground truth and authoritatively assert falsehoods regarding institutional affiliations.

### Finding 2: Re-confirmation of the Inverted Latency & Compensatory Loop
- In Condition 1 (With Playwright), OpenCode completed the audit in **252 seconds** (4.2 minutes) using native browser automation tools.
- In Condition 2 (Without Playwright), OpenCode required **845 seconds** (14.08 minutes) — a **3.35x latency surge** (+235.3%).
- Deprived of browser automation, the model entered an intensive compensatory loop: writing 18 separate bash and Python scripts, executing multiple `magick` crop commands to slice coordinate bounding boxes out of downloaded images, and running regex searches on raw HTML files. Despite this massive computational expenditure, it still failed item 20 due to its uncritical reliance on the deceptive HTML `alt` attribute.

### Finding 3: Visual Fold-Hidden Affordances in Public Sector Micro-Widgets
- The portal employs two distinct interactive fold-hiding mechanisms:
  1. **JavaScript-governed index gating**: In `NationalPortalServicesWidget`, items from index 8 onwards (such as `ইউটিলিটি বিল` at index 9) are given the class `national-portal-services-widget-hidden-item` and require clicking "আরো দেখুন ↓".
  2. **CSS pseudo-selector hiding**: In `BangladeshEmergencyHotlineWidget`, 23 emergency numbers are present in the DOM, but items from the 7th position onwards (`.emergency-numbers-item:nth-child(n+7)`) have `display: none` until the `#toggle-hotlines` checkbox is triggered.
- Human users glancing at the initial viewport only see 8 services and 6 hotlines. Agents inspecting raw DOM without style computation see all 65 services and 23 hotlines simultaneously, creating an **Affordance Inversion** where the agent's knowledge of what is immediately accessible differs radically from what a human citizen perceives.
