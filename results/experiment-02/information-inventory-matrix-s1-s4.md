# Information Inventory & Surface Grounding Matrix (Stage 3: S1–S4)

**Status:** Pre-registered ground truth for Stage 3 Multi-Domain Expansion.  
**Framework:** 4-Stage Human–Agent Information Accessibility Pipeline.  
**Evidence Sources:** Synchronized Human Visual Full-Page Captures (`data/stage-3/screenshots/`) and Machine DOM HTML (`data/stage-3/raw/`).  
**Pre-Registration Date:** 2026-10-19.

---

## 1. Experimental Framing

This inventory documents all human-observable information items on the four Stage 3 websites across four distinct web strata:
1. **S1 (E-Commerce & Retail)**: Star Tech Bangladesh (ASUS TUF Gaming Laptop)
2. **S2 (Professional Healthcare Services)**: Evercare Hospital Dhaka (Executive Health Check Package)
3. **S3 (Institutional & Public Portal)**: Gov.uk (Standard Visitor Visa)
4. **S4 (Technical Documentation & SaaS)**: Supabase (Pricing & Resource Limits)

Every item is tagged with its **Observable Modality Surface**:
- `TEXT`: Rendered HTML text in headers, descriptions, or tables.
- `IMAGE_TEXT`: Text or graphics embedded inside raster images/banners.
- `DYNAMIC`: Content rendered dynamically by client-side JavaScript or behind interactive clicks.
- `EXPLICIT_NEGATIVE`: Explicit statements of prohibition or incompatibility.
- `ABSENT`: Information unstated/missing from the page.

---

## 2. S1: Star Tech (E-Commerce & Retail)
- **Target URL:** `https://www.startech.com.bd/asus-tuf-gaming-a15-fa506ncg-ryzen-7-155-gaming-laptop`
- **Visual Capture:** [`data/stage-3/screenshots/S1-startech-fullpage.png`](../../data/stage-3/screenshots/S1-startech-fullpage.png) (1208 × 11,403 px)
- **Raw DOM File:** [`data/stage-3/raw/S1-startech-dom.html`](../../data/stage-3/raw/S1-startech-dom.html) (432.5 KB)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw DOM? | Target Research Check |
|---|---|---|---|---|---|
| S1-01 | Full Product Title & Model | `TEXT` | Header H1 | Yes | Entity extraction |
| S1-02 | Cash Discount Price (`144,000৳`) | `TEXT` | Top price badge & Radio option | Yes | Dual-price extraction |
| S1-03 | Regular Price (`153,780৳`) | `TEXT` | Top price badge & Radio option | Yes | Dual-price extraction |
| S1-04 | Explicit Stock Status (`In Stock`) | `TEXT` | Status badge beside price | Yes | Explicit stock statement (contrasts with Daraz) |
| S1-05 | Product Code (`53826`) & MPN (`FA506NCG-HN433W`) | `TEXT` | Header metadata & Key features | Yes | Structured metadata extraction |
| S1-06 | EMI Option (`12,815৳/mo` for up to 12 mo) | `TEXT` | Payment options block | Yes | Financing terms extraction |
| S1-07 | Free Delivery Promo Banner (Code `10.10`) | `IMAGE_TEXT` | Promo banner below gallery | **No** (Embedded in raster image) | **Gap 1: In-Image Tool Barrier** |
| S1-08 | Loyalty Points (`450 Star Points`) | `TEXT` | Reward points badge | Yes | Ancillary benefit extraction |
| S1-09 | Processor Specification (AMD Ryzen 7 155) | `TEXT` | Dedicated spec table | Yes | Spec table fidelity |
| S1-10 | Graphics Specification (RTX 3050 4GB GDDR6) | `TEXT` | Dedicated spec table | Yes | Spec table fidelity |
| S1-11 | Memory Specification (8GB DDR5-5600) | `TEXT` | Dedicated spec table | Yes | Spec table fidelity |
| S1-12 | Storage Specification (512GB PCIe 4.0 SSD) | `TEXT` | Dedicated spec table | Yes | Spec table fidelity |
| S1-13 | Display Specification (15.6" 144Hz FHD) | `TEXT` | Dedicated spec table | Yes | Spec table fidelity |
| S1-14 | Warranty Duration (`02 Years International Limited`) | `TEXT` | Spec table bottom row | Yes | Policy extraction |
| S1-15 | Incompatibility Exclusions | `ABSENT` | **Not stated on page** | **Not in DOM** | Negative overreach check (RQ4) |

---

## 3. S2: Evercare Hospital Dhaka (Professional Healthcare Services)
- **Target URL:** `https://www.evercarebd.com/dhaka/health_package/evercare-executive-health-check-for-male-female`
- **Visual Capture:** [`data/stage-3/screenshots/S2-evercare-fullpage.png`](../../data/stage-3/screenshots/S2-evercare-fullpage.png) (1208 × 2,946 px)
- **Raw DOM File:** [`data/stage-3/raw/S2-evercare-dom.html`](../../data/stage-3/raw/S2-evercare-dom.html) (238.1 KB)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw DOM? | Target Research Check |
|---|---|---|---|---|---|
| S2-01 | Package Title: `EXECUTIVE HEALTH CHECK (MALE / FEMALE)` | `TEXT` | Main heading | Yes | Service entity extraction |
| S2-02 | **Package Price: `18,000 BDT`** | `DYNAMIC` | Sub-heading below title | **No (Omitted from raw static DOM)** | **Gap 1: Client-Side JS Dynamic Barrier** |
| S2-03 | Kidney Function: `CREATININE-SERUM` | `TEXT` | Investigation list item 1 | Yes | Itemized diagnostic fidelity |
| S2-04 | Kidney Function: `UREA-SERUM` | `TEXT` | Investigation list item 2 | Yes | Itemized diagnostic fidelity |
| S2-05 | Uric Acid: `URIC ACID-SERUM` | `TEXT` | Investigation list item 3 | Yes | Itemized diagnostic fidelity |
| S2-06 | Cardiac Diagnostic: `ECG` | `TEXT` | Investigation list item 4 | Yes | Itemized diagnostic fidelity |
| S2-07 | Cardiac Diagnostic: `ECHO SCREENING` | `TEXT` | Investigation list item 5 | Yes | Itemized diagnostic fidelity |
| S2-08 | Hematology: `CBC` (Complete Blood Count) | `TEXT` | Investigation list item 6 | Yes | Itemized diagnostic fidelity |
| S2-09 | Hematology: `ESR` | `TEXT` | Investigation list item 7 | Yes | Itemized diagnostic fidelity |
| S2-10 | Blood Grouping: `ABO & RH GROUPING` | `TEXT` | Investigation list item 8 | Yes | Itemized diagnostic fidelity |
| S2-11 | Pulmonary Diagnostic: `SPIROMETRY (BASIC PFT TEST)` | `TEXT` | Investigation list item 9 | Yes | Itemized diagnostic fidelity |
| S2-12 | Radiology: `CHEST PA(X-RAY)` | `TEXT` | Investigation list item 10 | Yes | Itemized diagnostic fidelity |
| S2-13 | Stool Analysis: `STOOL-ROUTINE AND MICROSCOPY` | `TEXT` | Investigation list item 11 | Yes | Itemized diagnostic fidelity |
| S2-14 | Hematology: `COMMENT ON PERIPHERAL BLOOD SMEAR` | `TEXT` | Investigation list item 12 | Yes | Itemized diagnostic fidelity |
| S2-15 | Consultation Inclusion: `CONSULTATION FEE (0)` | `TEXT` | Investigation list item 13 | Yes | Free consultation inclusion |
| S2-16 | Liver Function: `LIVER FUNCTION TEST / PROFILE-SERUM` | `TEXT` | Investigation list item 14 | Yes | Itemized diagnostic fidelity |
| S2-17 | Diabetes Screening: `GLUCOSE ( FASTING )` | `TEXT` | Investigation list item 15 | Yes | Itemized diagnostic fidelity |
| S2-18 | Diabetes Screening: `GLUCOSE ( POST PRANDIAL )` | `TEXT` | Investigation list item 16 | Yes | Itemized diagnostic fidelity |
| S2-19 | Lipid Profile: `LIPID PROFILE -SERUM` | `TEXT` | Investigation list item 17 | Yes | Itemized diagnostic fidelity |
| S2-20 | Ultrasound: `ABDOMEN WHOLE (FEMALE) ULTRASONOGRAM` | `TEXT` | Investigation list item 18 | Yes | Gender-specific test inclusion |
| S2-21 | Urine Analysis: `URINE SUGAR (FASTING)` | `TEXT` | Investigation list item 19 | Yes | Itemized diagnostic fidelity |
| S2-22 | Urine Analysis: `URINE SUGAR (POST PRANDIAL)` | `TEXT` | Investigation list item 20 | Yes | Itemized diagnostic fidelity |
| S2-23 | Urine Analysis: `URINE PROFILE` | `TEXT` | Investigation list item 21 | Yes | Itemized diagnostic fidelity |
| S2-24 | Appointment Booking Hotline (`10678`) | `TEXT` | Header contact info | Yes | Contact affordance extraction |
| S2-25 | Interactive Booking Action (`Book Now` button) | `DYNAMIC` | Button below test roster | Yes | Booking affordance |

---

## 4. S3: Gov.uk (Institutional & Public Portal)
- **Target URL:** `https://www.gov.uk/standard-visitor`
- **Visual Capture:** [`data/stage-3/screenshots/S3-govuk-fullpage.png`](../../data/stage-3/screenshots/S3-govuk-fullpage.png) (1208 × 6,744 px)
- **Raw DOM File:** [`data/stage-3/raw/S3-govuk-dom.html`](../../data/stage-3/raw/S3-govuk-dom.html) (151.1 KB)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw DOM? | Target Research Check |
|---|---|---|---|---|---|
| S3-01 | Visa Category: `Standard Visitor` | `TEXT` | Page Title H1 | Yes | Legal entity extraction |
| S3-02 | Permitted Stay Duration (`Up to 6 months`) | `TEXT` | Overview paragraph 2 | Yes | Temporal limit extraction |
| S3-03 | Standard Visa Application Fee (`£135`; updated from `£120`) | `TEXT` | Fee section | Yes | Statutory fee extraction |
| S3-04 | Permitted: Tourism / Holidays / Vacations | `TEXT` | Permitted activities bullet 1 | Yes | Positive scope extraction |
| S3-05 | Permitted: Visiting Family or Friends | `TEXT` | Permitted activities bullet 2 | Yes | Positive scope extraction |
| S3-06 | Permitted: Volunteering up to 30 days | `TEXT` | Permitted activities bullet 3 | Yes | Bounded positive condition |
| S3-07 | Permitted: Transit to another country | `TEXT` | Permitted activities bullet 4 | Yes | Positive scope extraction |
| S3-08 | Permitted: Business meetings / interviews | `TEXT` | Permitted activities bullet 5 | Yes | Bounded business scope |
| S3-09 | Permitted: Study / placements up to 6 months | `TEXT` | Overview & study bullets | Yes | Bounded education scope |
| S3-10 | **Prohibition 1: Paid or unpaid work for UK company** | `EXPLICIT_NEGATIVE` | *"You cannot:"* bullet 1 | Yes | **Negative claim fidelity (RQ4)** |
| S3-11 | **Prohibition 2: Claiming public funds (benefits)** | `EXPLICIT_NEGATIVE` | *"You cannot:"* bullet 2 | Yes | **Negative claim fidelity (RQ4)** |
| S3-12 | **Prohibition 3: Living in UK via frequent visits** | `EXPLICIT_NEGATIVE` | *"You cannot:"* bullet 3 | Yes | **Negative claim fidelity (RQ4)** |
| S3-13 | **Prohibition 4: Marrying or civil partnership** | `EXPLICIT_NEGATIVE` | *"You cannot:"* bullet 4 | Yes | **Negative claim fidelity (RQ4)** |
| S3-14 | Mandatory Requirement: Proof of departure | `TEXT` | Eligibility section bullet 1 | Yes | Prerequisite extraction |
| S3-15 | Mandatory Requirement: Proof of sufficient funds | `TEXT` | Eligibility section bullet 2 | Yes | Prerequisite extraction |
| S3-16 | Mandatory Requirement: Return travel funding | `TEXT` | Eligibility section bullet 3 | Yes | Prerequisite extraction |

---

## 5. S4: Supabase (Technical Documentation & SaaS)
- **Target URL:** `https://supabase.com/pricing`
- **Visual Capture:** [`data/stage-3/screenshots/S4-supabase-fullpage.png`](../../data/stage-3/screenshots/S4-supabase-fullpage.png) (1208 × 16,384 px)
- **Raw DOM File:** [`data/stage-3/raw/S4-supabase-dom.html`](../../data/stage-3/raw/S4-supabase-dom.html) (385.9 KB)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw DOM? | Target Research Check |
|---|---|---|---|---|---|
| S4-01 | Free Tier Base Price (`$0 / month`) | `TEXT` | Free plan card header | Yes | Multi-tier base pricing |
| S4-02 | Free Tier Database Storage Quota (`500 MB`) | `TEXT` | Free plan card bullet 3 | Yes | Resource quota extraction |
| S4-03 | Free Tier RAM & CPU (`Shared CPU • 500 MB RAM`) | `TEXT` | Free plan card bullet 3 subtext | Yes | Resource quota extraction |
| S4-04 | Free Tier Egress Bandwidth (`5 GB egress`) | `TEXT` | Free plan card bullet 4 | Yes | Resource quota extraction |
| S4-05 | Free Tier Cached Egress (`5 GB cached egress`) | `TEXT` | Free plan card bullet 5 | Yes | Resource quota extraction |
| S4-06 | Free Tier File Storage Quota (`1 GB`) | `TEXT` | Free plan card bullet 6 | Yes | Resource quota extraction |
| S4-07 | Free Tier MAU Limit (`50,000 monthly active users`) | `TEXT` | Free plan card bullet 2 | Yes | Resource quota extraction |
| S4-08 | **Free Tier Auto-Pause Rule (1 week inactivity)** | `TEXT` | Free plan card footer note | Yes | Critical usage constraint |
| S4-09 | Free Tier Active Project Limit (`Limit of 2`) | `TEXT` | Free plan card footer note | Yes | Critical usage constraint |
| S4-10 | Pro Tier Base Price (`$25 / month`) | `TEXT` | Pro plan card header | Yes | Multi-tier base pricing |
| S4-11 | Pro Tier Included Projects (`First project included`) | `TEXT` | Pro plan card subtext | Yes | Multi-tier pricing structure |
| S4-12 | Pro Tier Extra Project Fee (`$10/mo per extra project`) | `TEXT` | Pro plan card subtext | Yes | Multi-tier pricing structure |
| S4-13 | Pro Tier Database Size (`8 GB disk size per project`) | `TEXT` | Pro plan card bullet 2 | Yes | Quantitative resource quota |
| S4-14 | Pro Tier Database Overage Rate (`$0.125 per GB`) | `TEXT` | Pro plan card bullet 2 subtext | Yes | Overage rate card extraction |
| S4-15 | Pro Tier Egress Quota (`250 GB egress`) | `TEXT` | Pro plan card bullet 3 | Yes | Quantitative resource quota |
| S4-16 | Pro Tier Egress Overage Rate (`$0.09 per GB`) | `TEXT` | Pro plan card bullet 3 subtext | Yes | Overage rate card extraction |
| S4-17 | Pro Tier File Storage (`100 GB file storage`) | `TEXT` | Pro plan card bullet 5 | Yes | Quantitative resource quota |
| S4-18 | Pro Tier File Storage Overage Rate (`$0.0213 per GB`) | `TEXT` | Pro plan card bullet 5 subtext | Yes | Overage rate card extraction |
| S4-19 | Pro Tier Backup Retention (`Daily backups for 7 days`) | `TEXT` | Pro plan card bullet 7 | Yes | Data protection spec |
| S4-20 | Pro Tier Log Retention (`7-day log retention`) | `TEXT` | Pro plan card bullet 8 | Yes | Observability spec |
| S4-21 | Pro Tier Add-on (Log Drains at `$60 per drain/mo`) | `TEXT` | Pro plan card bullet 9 | Yes | Add-on pricing extraction |
| S4-22 | Deep Feature Matrix Accordions | `DYNAMIC` | Collapsible table rows below | Yes | Accordion extraction fidelity |

---

## 6. Pre-Registration Summary

- **Total Audited Items Across S1–S4**: **74 discrete information items**
  - **S1 (Star Tech)**: 15 items
  - **S2 (Evercare Hospital)**: 25 items
  - **S3 (Gov.uk)**: 16 items
  - **S4 (Supabase)**: 22 items
- **Modality Breakdown**:
  - `TEXT` (Plain & Structured): 64 items
  - `DYNAMIC` (Client-side JS / Interactive): 4 items
  - `EXPLICIT_NEGATIVE` (Strict statutory prohibitions): 4 items
  - `IMAGE_TEXT` (In-image raster banner): 1 item
  - `ABSENT` (Unstated hardware facts): 1 item

This matrix is now frozen. All subsequent agent outputs in Stage 3 will be scored strictly against these 74 pre-registered items.
