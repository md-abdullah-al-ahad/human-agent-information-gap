# Pilot 01: provisional website observations

**Protocol:** [v0.2](audit-protocol.md) · **Site:** [Daraz Bangladesh](https://www.daraz.com.bd/) · **Collection:** 2026-10-17 18:56–19:10 UTC (2026-10-18 local time, Asia/Dhaka) · **Status:** exploratory AI and tool observations, awaiting independent human review. No formal model comparison or ground-truth accuracy score has been made.

## Selection and evidence

The live site's default search results supplied the first eligible distinct listing for each declared query. [Selection details](../data/pilot-01/selection.json) preserve the query, rank, URL, and limitation of the first search log. The selected listings were:

| Slot | Product page | Initial selected option and displayed price | Alternate option and displayed price |
| --- | --- | --- | --- |
| P1 | [Paper-Feel magnetic screen protector](https://www.daraz.com.bd/products/ipad-pro-11-129-esr-ipad-9-8-7-ipad-mini-6ipad-air-5-air-4-i373818784.html) | Air 5/4, ৳1,567 | Pro 10.5, ৳1,357 |
| P2 | [2PCS screen protector listing](https://www.daraz.com.bd/products/-i567669430.html) | Pro 11 M4, ৳872 | iPad A16 2025, ৳856 |
| P3 | [3+Y-fold iPad case](https://www.daraz.com.bd/products/-i567663291.html) | iPad Pro 11 2018–22, ৳1,223 | iPad Air 4/5/6/7 11, ৳1,217 |

These prices are observed page states, not current offers or product-wide prices. The alternate states were first reported after browser clicks; later independent loads of the resulting SKU URLs showed the same option labels and prices. See the [original observations](../data/pilot-01/observations.json), [append-only screenshot addendum](../data/pilot-01/addendum-01.json), and PNGs in [`data/pilot-01/screenshots/`](../data/pilot-01/screenshots/). The JSON records contain screenshot SHA-256 hashes.

**Methods.** A live Firecrawl browser session searched and inspected the pages, then clicked one alternate option per product. A separate Firecrawl `maxAge=0` markdown scrape requested each page with country `BD` and language `en`. Local headless Chrome for Testing 153 captured initial viewport screenshots and, later, alternate SKU URL screenshots at 1365×900. Exact browser tool prompts and returned prose outputs, along with the exact markdown returned by each scrape, are saved in [`data/pilot-01/raw/`](../data/pilot-01/raw/). The first P1 search result was transcribed into `selection.json`; its full raw search response was not retained. The live browser agent's prose is an AI report, not an independently verified rendering transcript.

**Protocol timing.** Q1–Q5 and the three sampling rules existed in v0.1 before collection. Q6–Q9 were added to v0.2 during this same session after initial site exposure, to capture price, availability, specifications, and variant behavior. This expansion is exploratory and was not preregistered or blinded; it cannot support a confirmatory comparison. A future formal run should freeze v0.2 questions before page access.

**Runtime metadata.** The investigating session identifies itself as Codex based on GPT-6; its exact deployed model ID, OpenRouter provider, and reasoning configuration were not exposed. Firecrawl's own browser-agent model and provider were also not exposed. The screenshots displayed a Daraz delivery location in Dhaka; this does not verify the browser's physical location. The scrape response reported a `BD` request location and an `America/New_York` service timezone. Formal comparison must explicitly align region, variant, and time.

## What the available evidence supports

- **Rendered title and prices were accessible.** All three initial screenshots visibly show title, selected option, price, and enabled Buy Now/Add to Cart controls. Each alternate screenshot shows a different selected option and price. These are successful retrievals by the browser/screenshot methods. The fact that purchase controls appear enabled does **not** establish stock.
- **The paper-feel listing exists in this sample.** P1 was the first displayed result for the paperlike query; its title explicitly says “Paper-Feel.” This is a listing claim about the surface, not verification of its physical texture or compatibility with every model named in the title.
- **Variants matter.** P1's selected option changed from Air 5/4 to Pro 10.5 and its price fell by ৳210. P2 and P3 also changed SKU URLs and displayed prices after a different option was selected. A title that names many iPad models cannot be treated as a statement that one selected SKU fits all of them.
- **Some listing fields were reported but remain provisional.** The browser report for P1 lists `Material: pet` and model compatibility text; P2 lists a generic `For Apple iPad` field; P3 lists case type, waterproof function, and Bengali material/feature text. The initial viewport screenshots do not show these lower-page fields. Human review should check exact wording, section, translation, and variant scope.

## Method differences, unsupported claims, and unknowns

| Observation | Evidence | Interpretation and limit |
| --- | --- | --- |
| Firecrawl markdown contained titles and some selected option labels, but no displayed price on any of the three pages. | [P1 scrape](../data/pilot-01/raw/P1-scrape.json), [P2 scrape](../data/pilot-01/raw/P2-scrape.json), [P3 scrape](../data/pilot-01/raw/P3-scrape.json); initial screenshots | **Method-specific retrieval omission.** It is not evidence that the prices were absent to a browser user. A dynamic rendering or extraction rule is a hypothesis, not an established cause. |
| The P1 browser report called the item “In Stock” while citing active purchase buttons; the screenshot shows buttons but no explicit stock statement. | [P1 browser report](../data/pilot-01/raw/P1-browser.json), [P1 screenshot](../data/pilot-01/screenshots/P1-initial.png) | **Unsupported inference in the exploratory tool response.** Explicit availability and actual stock remain unknown. No transaction was attempted. |
| The P2 browser report inferred glass material from a customer review. | [P2 browser report](../data/pilot-01/raw/P2-browser.json) | The review may describe one buyer's experience; it is not a dedicated product specification or independent material verification. The title's “Screen Protector Case ... Cover” wording also leaves included components ambiguous. |
| P1 scrape markdown says “No Ratings” while the initial screenshot shows “Ratings 1.” | [P1 scrape](../data/pilot-01/raw/P1-scrape.json), [P1 screenshot](../data/pilot-01/screenshots/P1-initial.png) | A cross-method discrepancy. Timing, personalization, or extraction error are possible; no cause is established. It does not establish a product-information failure on its own. |
| No explicit model incompatibility, paperlike claim on P2/P3, or Apple Pencil mention on P2/P3 was preserved in the inspected scope. | [Question observations](../data/pilot-01/observations.json) | **No page-wide negative conclusion.** Images, reviews, expandable details, translations, and all variants were not exhaustively checked. “Not observed here” is distinct from “the page does not state it,” and neither establishes a physical feature's absence. |

No whole-page access failure was seen: each selected URL loaded in the browser and returned HTTP 200 to the scrape. No false negative product or feature claim is established. No formal measure of unnecessary uncertainty is possible yet; the evidence does allow direct, qualified answers to simple title and price questions. The record does not support claims about real-world Apple Pencil performance, fulfillment, or stock.

## Possible causes to investigate later

These are **hypotheses**, not findings: (1) dynamic or client-rendered fields may be omitted by markdown extraction; (2) SKU changes may cause agents to conflate title-level claims with selected-variant facts; (3) source timing, locale, or extraction rules may explain the rating discrepancy; (4) ambiguous listing wording and machine translation may encourage unsupported product-type inferences. A controlled comparison with frozen page states is needed before assigning root causes.

## Human verification needed

1. Independently inspect the three URLs and selected SKU states in a logged-out browser; confirm title, price/currency, variant labels, and purchase-control state at a new recorded time. Prices may have changed.
2. Review all relevant page sections, images, and accessible expandable content for exact compatibility, material, paperlike, Apple Pencil, explicit incompatibility, and explicit stock wording. Mark the inspected scope before assigning `not_stated` or `supported_false`.
3. Check P2's product type and included components, the review-derived “glass” inference, and the Bengali text/translations on P2 and P3. Preserve original wording and independent translations.
4. Establish human reference answers for Q1–Q9, ideally with a second blinded review. Keep unresolved or variant-dependent cases unresolved.
5. Before formal AI evaluation, record the exact model ID, OpenRouter provider and reasoning settings where available; align prompts, variant, locale, retrieval access, and observation time. Do not score the investigating agent's own notes as an independent model run.

This pilot establishes that the chosen tools can retrieve some rendered product information and that a text extraction method can omit fields visible in browser screenshots. It does not estimate an information-gap rate or show how broadly these observations generalize.
