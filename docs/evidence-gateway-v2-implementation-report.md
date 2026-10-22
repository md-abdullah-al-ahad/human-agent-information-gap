# LWA-Web v2 implementation report — 2026-10-23

A working first version of the evidence gateway is implemented and available as a standalone MCP server and a gated CLI/host interface. **52 tests passed**, including the existing v1 tests and 37 v2 tests. This is implementation and component verification; no new paid-agent experiment or matched v1/v2 evaluation was run.

## Delivered

| Component | Implemented behavior |
| --- | --- |
| [Source store](../scripts/evidence_gateway/store.py) | Content-addressed HTML/image/JSON blobs, immutable hash-checked records, separate observation times, reusable indexes, SQLite query caches/audit, persistent session counters. Administrative registration confines resolved paths and symlinks to an allowed root and copies the bytes. |
| [Compiler](../scripts/evidence_gateway/compiler.py) | Bound DOM containers, heading context, ordered lists, separately tagged embedded/network JSON, exact source locations, image tiles, browser geometry, and explicit coverage limits. Neighboring or nested cards cannot contribute fields to another subject merely through ancestry. |
| [Typed resolver](../scripts/evidence_gateway/protocol.py) | Exact code/entity extraction; labeled numbers with Bengali digit normalization; ISO dates; list position; extractive procedures/sets; narrow explicit stock/compatibility statements. Qualifiers must occur in the bound context. |
| [Visual processing](../scripts/evidence_gateway/visual.py) | Cached overview orientation, bounded detailed crops, two Tesseract layout modes, original-pixel coordinates, disagreement reporting, and an optional versioned vision-command adapter. No known-asset answer annotations are imported. |
| [Acquisition](../scripts/evidence_gateway/acquisition.py) | Explicitly enabled HTTP/browser access, rendered DOM and computed visibility, screenshots and element geometry, bounded passive JSON, and one automatic browser escalation when needed. Offline resolution never fetches the web. |
| [Gateway and gate](../scripts/evidence_gateway/gateway.py) | Compact certificates, immutable replay, source/time comparisons, a killable resolution process, call/pixel budgets, exact-value and required-step checks, citation checks, currentness rechecked at emission, and trusted-host model-usage telemetry. |
| [MCP server](../scripts/mcp_evidence_gateway.py) | Exactly three tools: `resolve_evidence`, `inspect_evidence`, `verify_answer`, with [typed request schemas](../scripts/evidence_gateway/schemas.py). Crop inspection returns an actual image block. The legacy path-based MCP is a separate entry point. |
| [CLI](../scripts/evidence_gateway_cli.py) | Administrative `register`; `resolve`, `inspect`, `verify`, and enforced `answer` commands. The host path constructs its final artifact only from an accepted certificate. |
| Packaging | [Pinned dependencies](../requirements-v2.lock.txt), [usage and configuration guide](evidence-gateway-v2-usage.md), and a [reproducible local demo](../examples/lwa_v2_demo.py). |

## Verification

The [test log](evidence-gateway-v2-test-results.txt) records **52 passing tests in 14.679 seconds**, with the OCR and browser integration checks enabled. The Python environment used Python 3.13.14, FastMCP 4.1.3, Pillow 13.0.0, Beautiful Soup 4.15.0, and Playwright 1.64.1. Native checks used Chromium headless shell revision 1248 and the available Tesseract 5.5.3 runtime with English/Bangla data. Ruff checks and formatting were also run on the new code.

Tests cover immutable capture reuse, symlink/path rejection, deterministic replay, coupon/percentage binding, nested-field isolation, exact Bengali names, procedure completeness, position within a named list, conflicting JSON/page values, uncertain historical references, blocked access, stale-at-emission certificates, crop bytes and source hashes, session quotas, slow-adapter termination, the optional vision adapter's cache, and both in-process and standalone stdio MCP calls. Existing v1 evidence checks continue to pass.

A real local browser check loaded a synthetic page with a CSS-hidden conflicting code and a JavaScript-inserted visible code. Explicit browser mode and automatic HTTP-to-browser escalation returned the rendered code and saved its geometry. This does not establish coverage of arbitrary websites, lazy states, or anti-bot challenges.

The real OCR check exposed a useful uncertainty: the same generated pixels yielded `READN10` in one layout pass and `READN1O` in another. The gateway returned an ambiguous certificate with both readings rather than an asserted code. The fixture's known text was not supplied to the OCR or resolver. Agreement between two layout modes is still correlated evidence from one engine.

## Local size and replay result

The [saved smoke result](evidence-gateway-v2-smoke.json) comes from the local synthetic catalog demo, containing two neighboring offers and 200 unrelated catalog entries:

| Measure | Result |
| --- | ---: |
| Source HTML | 14,261 bytes |
| Indexed records | 202 |
| Returned certificate | 1,057 bytes |
| Certificate under `cl100k_base` | 350 tokens |
| First resolution, including optional token counting | 374.33 ms |
| Replayed resolution, including optional token counting | 230.76 ms |
| Certificate identical on replay | Yes |
| Differently worded question reused the index | Yes |
| Neighboring offer's wrong code passed the answer gate | No |

These are one fixture's component measurements. The certificate token count excludes tool schemas, conversation context, usage metadata, and image tokens. `cl100k_base` is not the pilot Qwen model's tokenizer. The smaller payload relative to raw HTML does **not** establish savings relative to the v1 tool or an end-to-end agent baseline. Timing includes a local tokenizer subprocess, is machine-specific, and should not be interpreted as a benchmark distribution.

## Boundaries that remain

- Extraction is deliberately bounded and rule-based. It requires a useful entity/container label and often a field label. The compiler currently uses one DOM parser, with separately retained structured data and visual readings; it does not claim independent multi-extractor consensus. General semantic relation extraction, multilingual paraphrase validation, and arbitrary visual logo ordering remain unresolved.
- Historical screenshots without DOM geometry use tiles and OCR orientation. Region discovery can still miss an item. No claim is made that the five v1 pilot failures are now fixed on their original captures.
- Visual-only answers are rejected by the final gate by default. A host can allow `corroborated_visual` answers, but OCR thresholds remain uncalibrated and model agreement does not guarantee correctness. The optional stronger vision adapter is implemented and fixture-tested; no paid vision provider is configured or evaluated.
- The process deadline bounds resolution work. Stored source bytes, screenshots, returned crop pixels, and tool calls are bounded; total browser network-transfer bytes are not a hard aggregate cap. Browser snapshots also leave interactive/lazy/iframe coverage incomplete.
- MCP cannot force an unrelated agent to use its final gate. Enforcement applies through `Gateway.answer()`, CLI `answer`, or a host that publishes only the accepted artifact. A client with other file/network tools needs separate isolation for a blinded evaluation.
- The 600–900-token architecture figure remains a design target. The implemented universal certificate ceiling is 6,000 UTF-8 bytes; optional exact counting requires a named tokenizer. Provider and host usage is explicitly reported rather than independently reconciled billing.

The next research validation is a matched comparison with independently adjudicated held-out references. The existing 15/20 score remains the **v1 offline pilot result**; there is no v2 agent accuracy score yet.
