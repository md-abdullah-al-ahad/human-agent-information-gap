# Stage 3 — Pilot reference-evidence adjudication, version 0.1

**Date:** 2026-10-18  
**Status:** **SECONDARY AI VISUAL REVIEW ONLY — INDEPENDENT HUMAN CONFIRMATION STILL PENDING**. This is not a final ground-truth set, a formal score, or a claim that the original agent answers are wrong about product reality.

## Scope and evidence provenance

This review directly inspected the original **human-captured PDF printouts**, rather than accepting the previous AI-generated PDF interpretations at face value:

| Slot | Original local capture | Pages | Product URL | Initial selected state |
|---|---|---:|---|---|
| P1 | 2026-10-18 01:22 Asia/Dhaka | 11 | https://www.daraz.com.bd/products/ipad-pro-11-129-esr-ipad-9-8-7-ipad-mini-6ipad-air-5-air-4-i373818784.html | `CHINA For iPad Air 5 4`, ৳1,567 |
| P2 | 2026-10-18 01:29 Asia/Dhaka | 6 | https://www.daraz.com.bd/products/-i567669430.html | `Pro 11 M4` with `2PCS`, ৳872 |
| P3 | 2026-10-18 01:39 Asia/Dhaka | 7 | https://www.daraz.com.bd/products/-i567663291.html | `YZ-YKL Black`, `iPad Pro 11 2018-22`, ৳1,223 |

The PDFs are user-uploaded conversation evidence, not committed to the repository. Their printable views include text and seller marketing images, but **cannot independently verify actual product performance, physical compatibility, inventory, shipment contents, or post-click variant state**. The six live shopping-agent traces were captured later the same day. Do not use the older PDF as if it were a contemporaneous snapshot of every agent interaction.

Source review files: `data/pilot-01/human-capture-P1-ai-review.json`, `...-P2-ai-review.json`, `...-P3-ai-review.json`. The pilot browser observations are also AI-generated and do **not** convert the PDFs into independent human-confirmed ground truth.

## Evidence vocabulary (use for all later annotation)

- **DISPLAYED** — a value or control visibly rendered in the captured state, e.g., selected SKU price.
- **SELLER_EXPLICIT** — a categorical statement in title, description, text or image, with *source scope* preserved.
- **SELLER_IMPLIED** — plausible interpretation of a visible image, UI affordance or incomplete list, not verbatim explicit support.
- **CONFLICTING** — two relevant listing surfaces make incompatible or apparently inconsistent claims; do not silently select one.
- **NOT_OBSERVED** — the inspected evidence does not contain this statement; this does **not** prove website-wide or real-world absence.
- **DYNAMIC_UNVERIFIED** — static capture does not prove a post-click change; a separately timestamped trace may support a different state.
- **EXTERNAL_UNVERIFIED** — performance, inventory, physical fit, true manufacturer, Pencil charging etc. not established by the seller's representation.

A *claim supported as a seller statement* is not an independently verified product fact. A *correct real-world guess* can still be unsupported as an answer purportedly derived only from this page.

## P1 — ESR magnetic paper-feel screen protector

| Q | PDF evidence and location | Correctly bounded reference judgment |
|---|---|---|
| Q1 identity | Title/description pages 1–2 call it ESR magnetic paper-feel detachable film; marketplace brand says `No Brand` on page 1 | **SELLER_EXPLICIT + CONFLICTING** for authenticity/brand; main product category supported as advertised. |
| Q2 models | General title/details pages 1–2 mention Pro 12.9, Pro 11, mini 6, 9/8/7, Air 4/5. Page 2 marketing image says **“Only compatible with”** Pro 11 (2018–2022) and Air 5/4; page 4 separate image says **“Compatible with”** those models. | **CONFLICTING scopes**. Do not equate an all-model title with any individual SKU, nor infer all title models are physically supported or excluded. |
| Q3 paperlike | Title, page-2 “Paper-Feel” image, pages 4–7 claims about drawing/texture | **SELLER_EXPLICIT** paper-feel/fine-texture advertisement; actual tactile quality untested. |
| Q4 unsupported models | Page 2 explicitly uses “Only compatible with” in one graphic while the product-level title/details are broader | A **bounded seller exclusion** is present for that graphic's apparent product version, but blanket physical incompatibility of every unlisted model is **NOT ESTABLISHED**. Particularly avoid definitive Pro 12.9 exclusion when general title/details mention it. |
| Q5 Pencil | Pages 3–7 describe drawing, notes, nib life, fine-texture | Seller markets stylus-like writing benefits; actual **Apple Pencil model compatibility not explicitly established** in the reviewed surfaces. |
| Q6 price | Page 1 `Air 5 4`, ৳1,567 | **DISPLAYED** for initial state only. |
| Q7 stock | Page 1 buy/cart controls; no explicit stock statement | **NOT_OBSERVED** inventory quantity/status. Buttons alone do not confirm inventory. |
| Q8 specs | Pages 1–2 PET, pack quantity, model “Universal”; “Size: 12.9” generic field; “ESR” in description versus “No Brand” | **SELLER_EXPLICIT**, with variant scope and brand mismatches. |
| Q9 variants | Page 1 initial SKU; no post-click PDF | **DYNAMIC_UNVERIFIED** in PDF. Separate logged browser interactions report Pro 10.5 at ৳1,357. |

## P2 — 2PCS iPad screen protector with ambiguous “case/cover” title

| Q | PDF evidence and location | Correctly bounded reference judgment |
|---|---|---|
| Q1 product/box | Page 1 title says `Screen Protector Case ... Cover`; pages 2 and 4 depict **glass screen protector**; page 5 Bengali “What’s in the box” text retains case/cover wording | Glass protector identity is a **SELLER_EXPLICIT** image claim; whether an additional case ships is **CONFLICTING / UNVERIFIED**, not a categorical “no case” fact. |
| Q2 compatibility | Page 1 title advertises base iPad A16; pages 3–4 model-number compatibility chart includes Pro 12.9 and Pro 13 but omits explicit base 11th-gen A16; separate A16 SKU exists in live agent traces | **CONFLICTING scopes** between title, illustration, and option list. A model mentioned in a diagram is not thereby guaranteed selectable; a model absent from a diagram isn't physically excluded. |
| Q3 paperlike | Pages 2–4 glass/HD seller materials; no paperlike text in printed view | Clear glass is **SELLER_EXPLICIT**; no paperlike claim **NOT_OBSERVED**. Avoid physical negative beyond seller presentation. |
| Q4 excluded models | Pages 3–4 chart positively lists Pro 12.9/13 despite lack of matching option in evaluated live selector | **No explicit categorical incompatibility** in source capture; missing selectable SKU ≠ verified incompatibility. |
| Q5 Apple Pencil | None found in six-page capture | **NOT_OBSERVED**; Pencil performance **EXTERNAL_UNVERIFIED**. |
| Q6 initial price | Page 1 Pro 11 M4/2PCS ৳872 | **DISPLAYED**. |
| Q7 stock | Page 1 buy/cart controls; no explicit stock statement | **NOT_OBSERVED** actual inventory. |
| Q8 specs/material | Pages 2–4 glass/HD/five marketing layers; page 5 `No Brand` and compatibility fields | **SELLER_EXPLICIT** marketing, not independently tested construction or shipment composition. |
| Q9 variant selection | PDF only shows initial Pro 11 M4. Later both agents explicitly selected A16 at ৳856 | **DYNAMIC_UNVERIFIED** in PDF, **observed in later dated traces**; keep evidence sources separate. |

## P3 — 3+Y-fold flip clear iPad case (Pencil-dispute audit)

**Direct independent inspection of original embedded images** (not merely prior AI JSON):

- PDF page **2**, seller's 1000×1000 gallery image: a long, narrow transparent side channel is visible beside the tablet; a small circular/opening-like region is visible near one end.
- PDF page **4**, seller's 1500×1500 “Crystal Clear Back Case” image: an oblong recess/channel along the case edge appears in the transparent frame.
- PDF page **3** seller's 1500×1500 usage collage shows a person using a white stylus *on* the tablet; that does not establish a holder or Pencil charging.
- No explicit `Apple Pencil`, `stylus holder`, `charging`, `Pencil slot` etc. statement was found in the printable listing text or examined marketing headings.
- **Interpretation:** the photographed channel is **consistent with** an integrated stylus tray, and should not be ignored. However, its function, orientation across SKUs, Pencil fit, finger ejection, magnetic attachment and charging are **NOT EXPLICITLY VERIFIED**. A product-in-hand or variant-specific labeled image would be needed for strong positive claims. The previous “no Pencil slot visible” phrasing is too categorical in light of this visual feature; the opposite categorical claim is also not independently confirmed.
- Crucially, distinguishing “I did not find evidence” from “there is no slot” matters for the eventual scoring rubric.

| Q | PDF evidence and location | Correctly bounded reference judgment |
|---|---|---|
| Q1 identity | Title/graphics pages 1–5: transparent-backed 3+Y-fold protective folio cover | **SELLER_EXPLICIT** case identity. |
| Q2 compatibility | Page 1 size selector includes base `iPad 11th A16 2025` separate from selected Pro 11 | **DISPLAYED** seller offered named sizes, not independently established fit. |
| Q3 included protector? | Page 5 says to peel protective film on **inner and outer of transparent case**; images show case | A **case transport film**, not proof of included screen protector. Strong contextual interpretation based on images; shipped-box contents never independently inventoried. |
| Q4 excluded models | No seller's exhaustive incompatibility list | **NOT_OBSERVED**; absent size SKU not conclusive physical incompatibility. |
| Q5 Pencil | Pages 2/4 show long transparent side channel; page 3 shows stylus use. No explicit text promising Pencil support | **SELLER_IMPLIED / AMBIGUOUS** storage-slot interpretation. **EXTERNAL_UNVERIFIED** specific charging/fit. Requires separate human check. |
| Q6 initial price | Page 1 Black + Pro 11 2018–22 ৳1,223 | **DISPLAYED**. |
| Q7 stock | Page 1 buttons/delivery text; no explicit stock field | **NOT_OBSERVED** inventory. |
| Q8 features | Pages 2–5 marketing: foldable stand, smart wake/sleep, PU leather, TPU, PC back, microfiber, scratch/drop claims; page 6 fields “Waterproof” | **SELLER_EXPLICIT** marketing, actual protection untested. |
| Q9 variant selection | Page 1 current Black/Pro selection; no post-click PDF | **DYNAMIC_UNVERIFIED** in PDF; two independent agent traces later observed Black/Air option at ৳1,217. |

## Provisional findings, not scores

1. Across six natural shopping runs on these three pages, both agent setups repeatedly stated “in stock” from purchase affordances. That is **unsupported inventory inference** relative to source statements, **not a proven wrong stock state**.
2. Nonlisted model → “incompatible” is an **evidence-scope overreach** in all three examples. Source claims differ, however: P1 actually has an “Only compatible with” marketing image; P2 image chart lists Pro 12.9/13 absent from observed SKU list; P3 has no explicit exhaustive exclusion.
3. The P3 Pencil disagreement cannot yet be scored as a simple binary right/wrong: the channel is visible, but its purpose and precise Pencil functions are not proven.
4. Both agents correctly identified requested live variant-specific prices in all three cases, based on their logged browsing interactions.
5. Some reasoning succeeds: case transport film is distinguishable from a screen protector (P3). We must retain successes in scoring to avoid failure-only selection bias.

## Human adjudication protocol (next action)

For each of 27 question–page slots, a person should **inspect the original PDF**, preferably while blinded to both agents' final answers. Record (a) statement quoted/paraphrased in the listing, (b) exact page and image/text region, (c) variant scope, (d) statement class above, (e) whether this answers *what the seller says* or establishes *external truth*, and (f) unclear/contradictory cases. If possible, use two independent annotators and reconcile disagreements, rather than having the assistant both propose labels and certify them.

**Priority manual checks:** P3 photographed stylus-channel function; P2 what actually ships with “2PCS”; P1 image restriction scope/variant. Do not force binary classification for ambiguous cases; allow `UNRESOLVED` with an explicit missing-evidence reason.

Maintain separate fields for:
- `evidence_accessed_by_agent`
- `support_given_observed_evidence`
- `supported_by_full_human_visible_page`
- `actual_product_truth_known`
- `answered_vs_abstained`
- `human_adjudication_status`

Once reviewed, freeze the reference protocol and candidate hypotheses on **new held-out pages** before computing performance rates. Do not label the six pilot outputs as a population estimate.
