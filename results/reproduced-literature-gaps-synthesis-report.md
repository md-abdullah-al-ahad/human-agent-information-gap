# Reanalysis of Existing Web-Agent Benchmark Artifacts

**Scope:** Four analyses of existing captures and the 1,010-row benchmark CSV. No new agent trial is represented by this report. The literature discussion in [`docs/deep-research-report-by-chatgpt.md`](../docs/deep-research-report-by-chatgpt.md) provides context; this report only states what the local scripts and saved result files support.

## 1. HTML Extractor Comparison

[`scripts/reproduce_extractor_disagreement.py`](../scripts/reproduce_extractor_disagreement.py) checks whether selected literal strings appear in the output of five extractors applied to four saved HTML files. Its "recall" is exact substring recovery on a small, hand-selected list, not general page-fact recall. The saved [`results/reproduced-extractor-disagreement-results.json`](reproduced-extractor-disagreement-results.json) contains:

| Extractor | Shwapno (17) | Nagad (14) | Shohoz (11) | Chaldal (10) | Mean processing time in saved run |
|---|---:|---:|---:|---:|---:|
| Trafilatura | 8/17 | 5/14 | 1/11 | 6/10 | 55.0 ms |
| Readability | 4/17 | 0/14 | 1/11 | 2/10 | 52.4 ms |
| BeautifulSoup | 14/17 | 9/14 | 9/11 | 7/10 | 44.5 ms |
| html2text | 14/17 | 9/14 | 8/11 | 7/10 | 47.3 ms |
| LWA DOM condenser | 15/17 | 9/14 | 9/11 | 8/10 | 16.8 ms |
| Five-output union | 15/17 | 9/14 | 9/11 | 8/10 | 216.0 ms (sum of extractor times) |

Readability omitted many selected strings in these application pages. The union recovered **zero additional selected items beyond the best individual extractor at every site**. The two Shwapno coupon strings and two Nagad bonus strings were among the missed items; the experiment did not test real image OCR. The former report's recall and latency figures for several sites did not match the saved JSON and have been withdrawn.

## 2. Shwapno API and Chaldal Embedded State

[`scripts/reproduce_dom_api_asymmetry.py`](../scripts/reproduce_dom_api_asymmetry.py) queried a Shwapno Algolia index and compared stringified field values with one saved 2,415,352-byte HTML file. Its [`saved results`](reproduced-dom-api-asymmetry-results.json) report:

| Returned product | Tested fields | Exact value strings found in saved HTML | Not found by this string test | Saved API hit bytes | Whole-HTML/API-hit size ratio |
|---|---:|---:|---:|---:|---:|
| Egg Loose | 24 | 5 | 19 (79.2%) | 4,954 | 487.6× |
| Alu (Potato) Regular Loose Kg | 21 | 5 | 16 (76.2%) | 12,237 | 197.4× |
| ACI Pure Salt 1kg | 23 | 8 | 15 (65.2%) | 7,093 | 340.5× |
| Finlays Masala Tea Bag in Bag 50gm | 24 | 7 | 17 (70.8%) | 5,383 | 448.7× |

These are **exact-string comparison results**, not proof that the fields were absent from a rendered page: values can be formatted differently, data can change between the saved page and the later API request, and the script searches raw HTML including embedded scripts. Comparing one product hit with an entire homepage is a payload-size illustration, not a lossless compression benchmark. The prior report's 1.2 KB payloads, approximately 1,900× ratios, and "zero information loss" claim contradict the saved JSON. The named tea product in that JSON is **Finlays**, not Fresh.

The Chaldal script parses `window.__serviceState` from the saved HTML itself. Its result shows 230 category names found in the HTML and 47 marketing banners in embedded state. Embedded state can hold fields that are not displayed to a person, but it is **present in the raw DOM file**; describing all of it as absent from the DOM is incorrect.

## 3. Claim-Support and Overreach Labels

The [`false-success analysis script`](../scripts/reproduce_false_success_and_overreach.py) now reads the master CSV and **only recounts existing label prefixes and selected pilot examples**. Its [`saved results`](reproduced-false-success-overreach-results.json) report 1,010 rows, 323 distinct IDs, and 16 rows whose human reference is not a positive visible fact. The previous version defaulted unmatched prose to `SUPPORTED`, assumed one claim per row, and produced invalid 100% claim precision and four-stage recall figures; those metrics have been withdrawn. Chaldal `BD2-20` records three agents saying "Fresh" where the case audit says the graphic shows MGI, while the CSV calls those rows `None` for gap classification.

The pilot case reports do support the narrower observation that all six Daraz agent answers asserted stock without an explicit stock statement, and that agents turned some absent selector options into physical-incompatibility claims. Those are evidence-support errors; the files do not verify actual warehouse stock or physical device fit. Counts across duplicate inventory/button rows must not be interpreted as independent errors. Failure transparency on Biman and Bdjobs is described in site reports, but Biman is a probe rather than one of the 323 scored items.

## 4. Temporal Labels on Shwapno and Nagad

[`scripts/reproduce_temporal_web_drift.py`](../scripts/reproduce_temporal_web_drift.py) contains 40 hand-entered baseline values, follow-up values, and statuses. When run, it counts those labels; it does not fetch a follow-up page or independently verify a change. Its [`saved JSON`](reproduced-temporal-web-drift-results.json) has 28 labeled `PERSISTED` and 12 labeled changed, giving **30% of this selected set**. That percentage is a summary of coded observations, not a measured live-web population rate.

The timestamps entered in the script are **2026-10-19 14:25 UTC** and **2026-10-21 01:30 UTC**, an interval of **35 hours 5 minutes (35.08 hours)**. The former "47.1 hours" and "48-hour" labels are arithmetically wrong. The Antigravity full transcript does preserve a narrower live observation: step 2531 records an Algolia query for four Shwapno products returning Egg Loose at 11, Alu at 27, ACI Pure Salt at 42, and a Finlays tea hit at 150. That query was logged at **2026-10-21 01:30 local time (+06:00)**, or **2026-10-20 19:30 UTC**; the script instead labels 01:30 as UTC. Thus the saved query supports those four API response values at that time, but does not verify the rendered homepage state, the Nagad changes, or the other follow-up labels. Separate follow-up DOM/screenshot captures and item-level evidence pointers are absent, so the 30% figure remains a count of hand-coded statuses rather than a validated live-web drift rate.

## 5. Status of the Proposed LWA-Web Design

The four analyses motivate combining rendered text, image inspection, structured data, and explicit uncertainty states. They do not validate the end-to-end [`LWA-Web prototype`](../scripts/lightweight_web_extractor.py) on unseen pages. Its current image enrichment injects prewritten strings for known asset names; it does not run OCR. The MCP wrapper can serve stored benchmark HTML for matching URLs. The proposed browser acquisition, automatic API interceptor, and execution circuit breaker are design work, not results of these four analyses.

See the [`repository consistency audit`](../docs/repository-consistency-audit.md) for the full correction ledger and remaining adjudication questions.
