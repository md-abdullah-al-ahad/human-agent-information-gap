# S2: Evercare Hospital Dhaka — Paired Agent & Tool Trace Audit (Track A)

**Status:** Completed empirical evaluation for S2 (Track A Live Browsing).  
**Evaluation Date:** 2026-10-19.  
**Evaluated Agents:**
1. **OpenCode / Qwen 3.8 27B Medium** (OpenRouter)
2. **Antigravity CLI / Gemini 3.8 Flash Medium** (Google)
**Tooling Environment:** Playwright MCP enabled for both setups.

---

## 1. Provenance and Runtime Metadata

| Measure | OpenCode / Qwen 3.8 27B | Antigravity / Gemini 3.8 Flash |
|---|---|---|
| **Session ID** | `ses_eaf5c84f3ffeeA8QNJU82FsMvS` | `8c7ce824-f848-4273-a696-cc933dbd14ad` |
| **Execution Timestamp** | 2026-10-19 02:10:45 Asia/Dhaka | 2026-10-19 02:11:07 Asia/Dhaka |
| **Total Playwright / Browser Calls** | **2**: `browser_navigate` (1), `browser_snapshot` (1) | **8**: `browser_navigate` (1), `browser_evaluate` (6), `browser_close` (1) |
| **Additional Tools Invoked** | None (pure single-pass accessibility snapshot) | File reads (output inspection, schema reads), worklog update |
| **Session Cost** | **$0.009700** (OpenRouter billed cost) | Billed per Google subscription (not exposed in export) |
| **Token Usage** | Input: 17,362 (cache read: 25,088); Output: 693; Reasoning: 1,252 | Input: ~42,000; Output: ~3,100 |
| **Raw Answer File** | [`opencode-qwen-user-exported-answer.md`](opencode-qwen-user-exported-answer.md) | [`antigravity-gemini-user-exported-answer.md`](antigravity-gemini-user-exported-answer.md) |
| **Full Session JSON** | [`opencode-qwen-session.json`](opencode-qwen-session.json) | [`antigravity-gemini-session.json`](antigravity-gemini-session.json) |

---

## 2. Evaluation Against Researcher-Annotated Reference (25 Items)

| Item ID | Target Information Item | Modality Surface | Human Ground Truth | Qwen Retrieved & Reported | Gemini Retrieved & Reported | Information Gap Classification |
|---|---|---|---|---|---|---|
| **S2-01** | Package Title | `TEXT` | `EXECUTIVE HEALTH CHECK (MALE / FEMALE)` | **Yes** (`EXECUTIVE HEALTH CHECK (MALE / FEMALE)`) | **Yes** (`EXECUTIVE HEALTH CHECK (MALE / FEMALE)`) | None (Retained) |
| **S2-02** | Package Price & Currency | `DYNAMIC` (original label; hydration dependence unverified) | `18,000 BDT` | **Yes** (`18,000 BDT`) | **Yes** (`18,000 BDT`) | None (retained by both agents; present in saved browser-captured DOM) |
| **S2-03** | Diagnostic: Creatinine | `TEXT` | `CREATININE-SERUM` | **Yes** (`CREATININE-SERUM`) | **Yes** (`CREATININE-SERUM`) | None (Retained) |
| **S2-04** | Diagnostic: Urea | `TEXT` | `UREA-SERUM` | **Yes** (`UREA-SERUM`) | **Yes** (`UREA-SERUM`) | None (Retained) |
| **S2-05** | Diagnostic: Uric Acid | `TEXT` | `URIC ACID-SERUM` | **Yes** (`URIC ACID-SERUM`) | **Yes** (`URIC ACID-SERUM`) | None (Retained) |
| **S2-06** | Cardiac: ECG | `TEXT` | `ECG` | **Yes** (`ECG`) | **Yes** (`ECG`) | None (Retained) |
| **S2-07** | Cardiac: Echo Screening | `TEXT` | `ECHO SCREENING` | **Yes** (`ECHO SCREENING`) | **Yes** (`ECHO SCREENING`) | None (Retained) |
| **S2-08** | Hematology: CBC | `TEXT` | `CBC` | **Yes** (`CBC`) | **Yes** (`CBC`) | None (Retained) |
| **S2-09** | Hematology: ESR | `TEXT` | `ESR` | **Yes** (`ESR`) | **Yes** (`ESR`) | None (Retained) |
| **S2-10** | Blood Grouping | `TEXT` | `ABO & RH GROUPING` | **Yes** (`ABO & RH GROUPING`) | **Yes** (`ABO & RH GROUPING`) | None (Retained) |
| **S2-11** | Pulmonary: Spirometry | `TEXT` | `SPIROMETRY (BASIC PFT TEST)` | **Yes** (`SPIROMETRY (BASIC PFT TEST)`) | **Yes** (`SPIROMETRY (BASIC PFT TEST)`) | None (Retained) |
| **S2-12** | Radiology: Chest X-Ray | `TEXT` | `CHEST PA (X-RAY)` / `CHEST PA(X-RAY)` | **Yes** (`CHEST PA (X-RAY)`) | **Yes** (`CHEST PA(X-RAY)`) | None (Retained) |
| **S2-13** | Stool Analysis | `TEXT` | `STOOL-ROUTINE AND MICROSCOPY` | **Yes** (`STOOL-ROUTINE AND MICROSCOPY`) | **Yes** (`STOOL-ROUTINE AND MICROSCOPY`) | None (Retained) |
| **S2-14** | Hematology: Blood Smear | `TEXT` | `COMMENT ON PERIPHERAL BLOOD SMEAR` | **Yes** (`COMMENT ON PERIPHERAL BLOOD SMEAR`) | **Yes** (`COMMENT ON PERIPHERAL BLOOD SMEAR`) | None (Retained) |
| **S2-15** | Consultation Line Item | `TEXT` | `CONSULTATION FEE (0)` | **Yes** (`CONSULTATION FEE (0)`) | **Yes** (`CONSULTATION FEE (0)`) | None (Retained; both explicitly noted lack of doctor details) |
| **S2-16** | Liver Function Profile | `TEXT` | `LIVER FUNCTION TEST / PROFILE-SERUM` | **Yes** (`LIVER FUNCTION TEST / PROFILE-SERUM`) | **Yes** (`LIVER FUNCTION TEST / PROFILE-SERUM`) | None (Retained) |
| **S2-17** | Glucose Fasting | `TEXT` | `GLUCOSE ( FASTING )` | **Yes** (`GLUCOSE (FASTING)`) | **Yes** (`GLUCOSE ( FASTING )`) | None (Retained) |
| **S2-18** | Glucose Post Prandial | `TEXT` | `GLUCOSE ( POST PRANDIAL )` | **Yes** (`GLUCOSE (POST PRANDIAL)`) | **Yes** (`GLUCOSE ( POST PRANDIAL )`) | None (Retained) |
| **S2-19** | Lipid Profile | `TEXT` | `LIPID PROFILE -SERUM` | **Yes** (`LIPID PROFILE-SERUM`) | **Yes** (`LIPID PROFILE -SERUM`) | None (Retained) |
| **S2-20** | Ultrasound Abdomen | `TEXT` | `ABDOMEN WHOLE (FEMALE) ULTRASONOGRAM (ULTRA SOUND)` | **Yes** (Exact verbatim match) | **Yes** (Exact verbatim match, flagged `(FEMALE)`) | None (Retained) |
| **S2-21** | Urine Sugar Fasting | `TEXT` | `URINE SUGAR (FASTING)` | **Yes** (`URINE SUGAR (FASTING)`) | **Yes** (`URINE SUGAR (FASTING)`) | None (Retained) |
| **S2-22** | Urine Sugar Post Prandial | `TEXT` | `URINE SUGAR (POST PRANDIAL)` | **Yes** (`URINE SUGAR (POST PRANDIAL)`) | **Yes** (`URINE SUGAR (POST PRANDIAL)`) | None (Retained) |
| **S2-23** | Urine Profile | `TEXT` | `URINE PROFILE` | **Yes** (`URINE PROFILE`) | **Yes** (`URINE PROFILE`) | None (Retained) |
| **S2-24** | Booking Hotline | `TEXT` | `10678` (tel: `+8809606316505`) | **Yes** (`10678`, noted tel link) | **Yes** (`10678`, noted tel link) | None (Retained) |
| **S2-25** | Interactive Booking Action | `DYNAMIC` | `Book Now` button linking to appointment form | **Yes** (Extracted button and target URL) | **Yes** (Extracted button and target URL) | None (Retained) |

---

## 3. Key Empirical Findings on S2

1. **Flawless Itemized Medical Extraction (25/25 Items, 100% Retention)**:
   - Both agents successfully extracted all 20 clinical diagnostic investigations, the consultation fee line item, the package title, price, booking button, and phone hotline.
   - No diagnostic tests were omitted, truncated, or hallucinated.

2. **Package Price Retained; Hydration Mechanism Not Established by the Saved Artifacts**:
   - The saved `data/stage-3/raw/S2-evercare-dom.html` includes the price as visible HTML (`<h3 class="package-price ...">18,000 BDT</h3>`) and in embedded page state. It is a browser-captured DOM, not a frozen initial HTTP response.
   - Both agents reported `18,000 BDT`. Without a preserved static HTTP response from the same page state, this case cannot establish a static-versus-browser price gap or prove that client-side hydration was required.

3. **Restraint and Avoidance of Affordance Overreach on Unstated Consultations**:
   - The user prompt explicitly asked: *"Any consultations or physician reviews included?"*
   - In previous tests (e.g., Pilot 01), agents frequently overreached when presented with ambiguous or unstated fields.
   - On S2, the live page lists only `CONSULTATION FEE (0)` with no physician name, specialty, or consultation protocol.
   - Both agents demonstrated appropriate restraint:
     - Qwen reported: *"The page does not state any specific consultation type or named physician review. The only consultation-related item listed is 'CONSULTATION FEE (0)' within the included-items list."*
     - Gemini reported: *"Not stated on the page. The page does not name any specific doctor, medical specialty, clinical review protocol, or follow-up consultation process beyond the line item CONSULTATION FEE (0)."*
   - Neither model hallucinated clinical review details.

4. **Tool Strategy Comparison**:
   - **OpenCode / Qwen**: Executed a single `browser_navigate` followed immediately by a single `browser_snapshot`. The snapshot captured the entire rendered accessibility tree (208 elements), from which Qwen synthesized its response in one pass for **$0.009700**.
   - **Antigravity / Gemini**: Navigated via `browser_navigate`, viewed the snapshot YAML, and executed multiple targeted `browser_evaluate` JavaScript calls to verify dropdown menus, container hierarchies, and check for hidden tabs or accordions before closing the browser session cleanly.
