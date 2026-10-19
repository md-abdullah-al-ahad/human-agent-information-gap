Based on a direct inspection of the live webpage ([Evercare Hospital Dhaka - Executive Health Check](https://www.evercarebd.com/dhaka/health_package/evercare-executive-health-check-for-male-female)), here are the findings with citations to the corresponding page elements:

---

### 1. Full Title of the Health Package
* **Displayed Title on Page**: `EXECUTIVE HEALTH CHECK (MALE / FEMALE)`
  * **Element / Section**: Main page heading `<h1>` with class `package-title mb-4 text-2xl font-bold !text-primary`, as well as the active item in the breadcrumb navigation (`nav[aria-label="Breadcrumb"] ol li span`).
* **HTML Document Title (`<title>`)**: `Executive Health Check (Male/Female) | Evercare Hospital Dhaka`

---

### 2. Price and Currency Displayed
* **Displayed Price and Currency**: `18,000 BDT`
  * **Price**: `18,000`
  * **Currency**: `BDT` (Bangladeshi Taka)
  * **Element / Section**: Subheading `<h3>` directly beneath the package title, with class `package-price mt-7 text-2xl font-bold text-everblue-dark`.

---

### 3. Diagnostic Tests and Laboratory Investigations Included
All items are itemized within the unordered list element `<ul class="package-list">` under `<div class="package-list-content prose max-w-none">`. The 20 diagnostic tests and laboratory investigations are:

#### Laboratory Investigations (Blood, Urine, Stool)
1. `CREATININE-SERUM`
2. `UREA-SERUM`
3. `URIC ACID-SERUM`
4. `CBC`
5. `ESR`
6. `ABO & RH GROUPING`
7. `STOOL-ROUTINE AND MICROSCOPY`
8. `COMMENT ON PERIPHERAL BLOOD SMEAR`
9. `LIVER FUNCTION TEST / PROFILE-SERUM`
10. `GLUCOSE ( FASTING )`
11. `GLUCOSE ( POST PRANDIAL )`
12. `LIPID PROFILE -SERUM`
13. `URINE SUGAR (FASTING)`
14. `URINE SUGAR (POST PRANDIAL)`
15. `URINE PROFILE`

#### Diagnostic Imaging and Physiological Investigations
16. `ECG`
17. `ECHO SCREENING`
18. `SPIROMETRY (BASIC PFT TEST)`
19. `CHEST PA(X-RAY)`
20. `ABDOMEN WHOLE (FEMALE) ULTRASONOGRAM (ULTRA  SOUND)` *(Note: Stated verbatim on the page with "(FEMALE)")*

---

### 4. Consultations or Physician Reviews Included
* **Displayed Line Item**: `CONSULTATION FEE (0)`
  * **Element / Section**: Listed as the 13th item in `<ul class="package-list">`.
* **Physician / Specialty Details**: **Not stated on the page**. The page does not name any specific doctor, medical specialty, clinical review protocol, or follow-up consultation process beyond the line item `CONSULTATION FEE (0)`.

---

### 5. Booking and Appointment Process
According to the page, a patient can book or inquire through the following channels:

1. **Online Appointment Request**:
   * **Element**: A dedicated "Book Now" button located directly beneath the package test list:
     `<a href="/en/dhaka/appointment?package_name=evercare-executive-health-check-for-male-female&package_id=2"><button>Book Now</button></a>`
   * Clicking this button directs the patient to Evercare Dhaka's appointment booking form pre-populated with this specific package name and ID (`package_id=2`).
2. **Telephone Hotline**:
   * **Element**: The assistance callout section immediately below the "Book Now" button (`<div class="mb-2 mt-10 text-center lg:mt-20">`), which states:
     > *"For assistance and more information."*  
     > *"Please call 10678"* (`<a href="tel:+8809606316505">10678</a>`)
3. **General Inquiry Options Displayed on the Page**:
   * Header phone link: `10678` (`tel:+8809606316505`)
   * "Send Query" button linking to `/en/dhaka/query`
   * Footer contact email: `info@evercarebd.com`
   * Online portal link: `Evercare Tele Online` (`https://ecare.evercarebd.com:8000/`)

---

Log updated: `/home/abdullah/.agent_worklogs/general/2026-10.log.md`