# Stage 3 — Multi-Domain Website Selection & Audit Tasks (v0.1)

**Status:** Pre-registered website selection for Stage 3 Multi-Domain Expansion.  
**Selection Date:** 2026-10-18.  
**Sampling Balance:** 2 Bangladesh real-world websites + 2 International standard platforms to ensure empirical generalizability.

---

## 1. Selected Sites and Canonical URLs

| Stratum | Organization / Domain | Category | Canonical Target URL | Access Status |
|---|---|---|---|---|
| **Stratum 1** | **Star Tech** (Bangladesh) | E-Commerce & Retail | `https://www.startech.com.bd/asus-tuf-gaming-a15-fa506ncg-ryzen-7-155-gaming-laptop` | Verified HTTP 200 |
| **Stratum 2** | **Evercare Hospital Dhaka** (Bangladesh) | Healthcare & Professional Services | `https://www.evercarebd.com/dhaka/health_package/evercare-executive-health-check-for-male-female` | Verified HTTP 200 |
| **Stratum 3** | **Gov.uk** (United Kingdom) | Public & Institutional Portal | `https://www.gov.uk/standard-visitor` | Verified HTTP 200 |
| **Stratum 4** | **Supabase** (International) | Technical Documentation & SaaS | `https://supabase.com/pricing` | Verified HTTP 200 |

---

## 2. Stratum Rationale and Audit Targets

### Site 1: Star Tech (E-Commerce & Retail)
- **URL:** `https://www.startech.com.bd/asus-tuf-gaming-a15-fa506ncg-ryzen-7-155-gaming-laptop`
- **Why Selected:** Prominent Bangladeshi electronics retailer with high dynamic content, contrasting cash vs. regular pricing, explicit stock badges, and tabular specifications.
- **Specific Information Surfaces to Audit**:
  1. Cash Discount Price (`144,000৳`) vs. Regular Price (`153,780৳`).
  2. Monthly EMI breakdown (`12,815৳/month`).
  3. Explicit Stock Status (`In Stock` badge) — contrasts with Daraz where explicit stock text was absent.
  4. Hardware Specifications: Processor (AMD Ryzen 7 7435HS / 155), GPU (RTX 3050 4GB), RAM (16GB DDR5), Storage (512GB SSD), Display (15.6" 144Hz FHD).
  5. Warranty Terms (2 years official international warranty).
- **User Task Prompt**:
  *"I want to buy the ASUS TUF Gaming A15 FA506NCG laptop from Star Tech. What are the cash and regular prices, is it explicitly in stock, what are the exact CPU/GPU/RAM specifications, what warranty is offered, and what EMI options are visible?"*

---

### Site 2: Evercare Hospital Dhaka (Professional Healthcare Services)
- **URL:** `https://www.evercarebd.com/dhaka/health_package/evercare-executive-health-check-for-male-female`
- **Why Selected:** Leading healthcare provider in Bangladesh. Real-world service package with itemized diagnostic clinical tests, multi-item list structures, preparation guidelines, and booking affordances.
- **Specific Information Surfaces to Audit**:
  1. Service Identity: Executive Health Check (Male / Female).
  2. Itemized Clinical Tests: Complete enumeration of all 21 laboratory/diagnostic investigations (Creatinine, Urea, Uric Acid, ECG, Echo Screening, CBC, ESR, ABO & Rh grouping, Chest X-ray, Stool R/E, Fasting Blood Sugar, etc.).
  3. Consultation Inclusions: Physical examination, physician review, dietary advice.
  4. Pricing & Booking Affordances: Check whether package price is explicitly stated or requires phone consultation (`10678` / online portal).
- **User Task Prompt**:
  *"What tests are included in the Evercare Executive Health Check package in Dhaka? List all specific diagnostic investigations mentioned, identify what consultations are included, report the price if displayed, and state how a patient books the appointment."*

---

### Site 3: Gov.uk Standard Visitor Visa (Institutional & Public Portal)
- **URL:** `https://www.gov.uk/standard-visitor`
- **Why Selected:** The global gold standard for public digital service design. Contains structured criteria, fee schedules, duration limits, and **critical explicit negative prohibitions** to test false-absence and negative overreach (RQ4).
- **Specific Information Surfaces to Audit**:
  1. Visa Fee: Explicit current application fee (£120).
  2. Permitted Stay Duration: Standard maximum stay (up to 6 months).
  3. Positive Permitted Activities: Tourism, visiting family, business meetings, short courses (under 30 days).
  4. **Explicit Negative Prohibitions (What you CANNOT do)**:
     - Cannot do paid or unpaid work for a UK company.
     - Cannot claim public funds (benefits).
     - Cannot live in the UK through frequent or successive visits.
     - Cannot marry or register a civil partnership (requires Marriage Visitor visa).
  5. Mandatory Eligibility Evidence: Proof of funds, proof of intent to leave at end of visit.
- **User Task Prompt**:
  *"What are the rules for a UK Standard Visitor Visa on Gov.uk? State the application fee, maximum duration of stay, exactly what activities you are permitted to do, and explicitly quote what activities the page states you are NOT allowed to do."*

---

### Site 4: Supabase Pricing (Technical Documentation & SaaS)
- **URL:** `https://supabase.com/pricing`
- **Why Selected:** High-complexity developer pricing matrix with multi-tier tabular columns (Free vs. Pro vs. Team vs. Enterprise), quantitative compute/storage thresholds, overage fee calculations, and expandable feature accordions.
- **Specific Information Surfaces to Audit**:
  1. Tier Base Prices: Free ($0/mo), Pro ($25/mo), Team ($599/mo).
  2. Quantitative Database Storage Quotas: Free (500MB) vs. Pro (8GB included, then $0.125/GB).
  3. Egress Bandwidth Limits: Free (5GB/mo) vs. Pro (250GB/mo included, then $0.09/GB).
  4. Compute Hours & Pausing Rules: Active project hours and auto-pausing behavior on Free tier after inactivity.
  5. Expandable / Footnote Details: Daily backup retention vs. Point-in-time recovery (PITR) add-on.
- **User Task Prompt**:
  *"Using Supabase's pricing page, compare the Free and Pro plans. What are their monthly base prices, database storage limits, bandwidth egress limits, project auto-pause rules, and overage fees?"*

---

## 3. Next Execution Steps

1. **Freeze Ground Truth**: Execute headless visual and DOM captures of the four canonical URLs.
2. **Build Pre-Registered Information Inventories**: Itemize each page's discrete facts into `data/stage-3/` before running models.
3. **Generate Track B Packets**: Build B1 (text/DOM only) and B2 (text + raw image assets) packets for each site.
4. **Execute Trials**: Run OpenCode (Qwen 3.8 27B) and Antigravity (Gemini 3.8 Flash) across Track A (live browsing) and Track B (sealed packets).
