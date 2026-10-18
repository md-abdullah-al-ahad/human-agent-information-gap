# Stage 3 — Human-Accessible Information Reference & Surface Grounding (v0.2)

**Status:** Methodological alignment for Stage 3.  
**Purpose:** Establishes the grounded reference of **what is human-accessible on the captured webpages** across rendered text, image graphics, and interactive affordances.  
**Correction:** This document explicitly avoids model-versus-model evaluation or external physical truth claims. Its sole objective is to provide the empirical ground truth of the *website's observable information surfaces* to measure tool exposure and agent retrieval.

---

## 1. Information Surfaces and Evidence Vocabulary

A webpage is not a flat string of text; it is a multi-layered interface with distinct evidence surfaces:

1. **DISPLAYED**: Visible UI values, rendered typography, prices, currency, or active buttons in the captured state.
2. **SELLER_EXPLICIT_TEXT**: Categorical text statements in titles, bullet points, expandable descriptions, or structured specification tables.
3. **IN_IMAGE_GRAPHIC**: Text, diagrams, layer breakdowns, or specification charts embedded inside raster images/banners (invisible to plain DOM scrapers without OCR/vision tools).
4. **IMAGE_VISUAL_AFFORDANCE**: Physical appearance, shapes, or design features visible in product photographs without accompanying explanatory text.
5. **DYNAMIC_STATE**: Information exposed only after user interaction (e.g., clicking a variant thumbnail, opening an accordion, or checking a dropdown).
6. **SILENT_OR_ABSENT**: An information field that is entirely omitted from the page (e.g., explicit warehouse stock quantities, or negative compatibility exclusions).

---

## 2. Grounded Surface Reference for Pilot Pages

### P1: ESR Magnetic Screen Protector
- **Capture Source:** 11-page human browser print-to-PDF (`2026-10-18 01:22 Asia/Dhaka`).
- **Surface Breakdown**:
  - `Title & Identity`: Detachable magnetic screen protector for iPad. (SELLER_EXPLICIT_TEXT, p. 1).
  - `Brand Conflict`: Header field states `No Brand` (p. 1); description text states `ESR` (p. 2). Both are observable seller statements; neither confirms third-party authenticity.
  - `Model Compatibility in Text`: Title and description mention iPad Pro 11, Pro 12.9, 9/8/7, mini 6, Air 4/5. (SELLER_EXPLICIT_TEXT, pp. 1–2).
  - `Restrictive Model Scope in Graphics`: Marketing image explicitly states **"Only compatible with"** iPad Pro 11 (2018–2022) and iPad Air 5/4. (IN_IMAGE_GRAPHIC, p. 2).
  - `Surface Claim`: Advertised as "Paper-Feel" with drawing/writing fine texture. (SELLER_EXPLICIT_TEXT + IN_IMAGE_GRAPHIC, pp. 1, 4–7).
  - `Initial Pricing`: `CHINA For iPad Air 5 4` displayed at `৳1,567` with `৳1,881` crossed out (-17%). (DISPLAYED, p. 1).
  - `Inventory Status`: Active "Buy Now" and "Add to Cart" controls appear. Explicit numerical stock or stock status text is absent. (SILENT_OR_ABSENT).
  - `Specification`: Material listed as `PET`. (SELLER_EXPLICIT_TEXT in table, p. 2).

### P2: 2PCS Screen Protector with "Case/Cover" in Title
- **Capture Source:** 6-page human browser print-to-PDF (`2026-10-18 01:29 Asia/Dhaka`).
- **Surface Breakdown**:
  - `Form Factor & Naming`: Title reads "2PCS Screen Protector Case ... Cover" (SELLER_EXPLICIT_TEXT, p. 1). Primary photographs depict transparent glass screen protectors (IN_IMAGE_GRAPHIC, pp. 2, 4). "What's in the box" repeating the title leaves bundled contents ambiguous.
  - `Initial Pricing`: `Color: Pro 11 M4`, `Keyboard language: 2PCS` displayed at `৳872` (crossed out `৳2,266`). (DISPLAYED, p. 1).
  - `Detailed Compatibility Chart`: Visual matrix illustrates model numbers across Pro 12.9, Pro 13, Air 13, and others. (IN_IMAGE_GRAPHIC, pp. 3–4).
  - `Surface Texture`: Glossy, high-definition clear glass. No paperlike or matte claims exist. (IN_IMAGE_GRAPHIC + SELLER_EXPLICIT_TEXT).
  - `Stylus Mention`: No explicit Apple Pencil compatibility statement appears in the readable page scope. (SILENT_OR_ABSENT).
  - `Inventory Status`: Buy/cart controls are active. No stock count or explicit stock text exists. (SILENT_OR_ABSENT).

### P3: 3+Y-fold Clear Folio Case
- **Capture Source:** 7-page human browser print-to-PDF (`2026-10-18 01:39 Asia/Dhaka`).
- **Surface Breakdown**:
  - `Product Identity`: Transparent-backed folding protective iPad folio cover/case. (SELLER_EXPLICIT_TEXT + IN_IMAGE_GRAPHIC, pp. 1–5).
  - `Transit Film Instruction`: Section advises peeling protective film from the inner and outer surfaces of the transparent case. (SELLER_EXPLICIT_TEXT, p. 5).
  - `Initial Pricing`: `YZ-YKL Black`, `iPad Pro 11 2018-22` displayed at `৳1,223` (crossed out `৳3,086`). (DISPLAYED, p. 1).
  - `Visual Stylus Channel`: Gallery images (pp. 2, 4) show a dedicated transparent recess/channel along the side of the case frame. (IMAGE_VISUAL_AFFORDANCE).
  - `Stylus Text / Charging Claims`: No text explicitly promises Apple Pencil storage, magnetic pairing, or wireless charging. (SILENT_OR_ABSENT in text).
  - `Inventory Status`: Enabled purchase controls; no explicit stock quantity or availability text. (SILENT_OR_ABSENT).

---

## 3. Methodological Role in the Information Gap Research

This grounded reference serves as the benchmark against which agent performance is measured:

1. **Measuring Tool Exposure (Gap 1)**:
   - Does a standard DOM snapshot expose `IN_IMAGE_GRAPHIC` elements? (No: requires image download + OCR/vision).
2. **Measuring Agent Exploration (Gap 2)**:
   - Does an agent inspect all selector options, or only click a single variant?
   - Does an agent fetch images when critical information is absent from text?
3. **Measuring Output Reporting & Inference (Gap 3)**:
   - When a field is `SILENT_OR_ABSENT` (such as inventory stock), does the agent acknowledge the lack of information, or make an overconfident assertion based on button state?
   - When an unlisted model is absent from the variant list, does the agent distinguish "not offered in this selector" from "physically incompatible with the device"?
