# Running LWA-Web v2

The v2 server is [`scripts/mcp_evidence_gateway.py`](../scripts/mcp_evidence_gateway.py). It exposes exactly `resolve_evidence`, `inspect_evidence`, and `verify_answer`. The older `mcp_lite_extractor.py` remains the historical v1 server; starting it does not activate the v2 contracts.

## Install and check

From the repository root, use the pinned environment tested with Python 3.13:

```sh
uv venv --python 3.13 .venv-lwa-v2
uv pip sync --python .venv-lwa-v2/bin/python requirements-v2.lock.txt
.venv-lwa-v2/bin/python -m unittest discover -s tests -v
.venv-lwa-v2/bin/python examples/lwa_v2_demo.py
```

The demo creates a synthetic catalog locally, resolves the 7% offer, replays the same certificate, reuses the index for a differently worded question, and rejects the neighboring 9% offer's code. It makes no live request or model call. The demo's sources and certificates persist in the configured store so evidence handles remain inspectable.

Browser acquisition is optional. Install the matching browser while retaining other projects' cached runtimes:

```sh
PLAYWRIGHT_SKIP_BROWSER_GC=1 .venv-lwa-v2/bin/playwright install chromium --only-shell
```

OCR additionally requires Tesseract and the requested language files. Set `LWA_V2_TESSERACT` to its binary and `TESSDATA_PREFIX` to the language-data directory when they are not installed in the usual locations. `LWA_V2_OCR_LANG` defaults to `eng+ben`. A private runtime may also need its library directory in `LD_LIBRARY_PATH`. Missing OCR produces an explicit unresolved result.

The browser and OCR integration checks are opt-in because those native runtimes are separate from the Python lockfile:

```sh
LWA_V2_TEST_BROWSER=1 LWA_V2_TEST_OCR=1 .venv-lwa-v2/bin/python -m unittest discover -s tests -v
```

The OCR integration image is generated locally. Depending on the installed OCR runtime, it may yield agreement or a `0`/`O` disagreement; the contract requires a correct corroborated value or explicit ambiguity, never the wrong asserted code.

## Register a saved capture

Registration is an administrative CLI operation. Agent tools cannot register paths or change the allowed root.

```sh
.venv-lwa-v2/bin/python scripts/evidence_gateway_cli.py register \
  --root /absolute/path/to/answer-free-packet \
  --html page.html \
  --image screenshot.png \
  --captured-at 2026-10-21T00:00:00Z \
  --url https://example.org/page
```

Use an actual known capture time, or omit `--captured-at` when it is unknown. All file paths resolve beneath `--root`, including symlinks. Registration copies and hashes the bytes. Later source-file edits cannot silently change the saved capture. The output contains a `snapshot:...` handle for the agent and a reusable `capture:...` content identity.

Store selection is `--store PATH` on the CLI or `LWA_V2_STORE` in the server environment. The default is `~/.cache/lwa-web/v2`. Use a separate store containing only the approved packet for a blinded evaluation. This is a tool-level boundary; a client with independent shell/file tools still requires its own OS/container isolation.

## Resolve and gate an answer

Save a request like this, replacing the handle with registration output:

```json
{
  "source": {"kind": "snapshot", "id": "snapshot:REPLACE_WITH_REGISTERED_HANDLE"},
  "question": "What is the code for the 7% travel offer?",
  "answer_type": "exact_code",
  "subject": "Travel offer",
  "qualifiers": {"discount": "7%"},
  "scope": "page",
  "as_of": "capture",
  "budget": {"max_wall_ms": 20000, "max_visual_regions": 3, "max_ocr_calls": 4, "max_vision_calls": 0}
}
```

```sh
.venv-lwa-v2/bin/python scripts/evidence_gateway_cli.py resolve < request.json
.venv-lwa-v2/bin/python scripts/evidence_gateway_cli.py answer < request.json
```

`resolve` returns a certificate and measured usage. `answer` additionally invokes the answer gate and emits a final answer artifact only when the configured evidence policy accepts it. A host integrating `Gateway` should use `answer()` or pass a proposed exact value and citations through `verify()` before publishing the result. Free-form agent explanations are outside this gate.

The certificate is deterministic for the same registered source, typed request, and versioned processing configuration. Usage fields such as elapsed time and cache hits are deliberately outside the certificate and vary per invocation. Acquisition-event IDs and times are separate from content identity. A new live acquisition is a new observation even if its bytes match an older capture.

`subject` is an exact entity/container label expected in the evidence, not a complete natural-language question. `field` selects a source label such as `Name`, `Price`, or `Downloads`. Qualifier values must occur in the same bound source context. Query wording influences retrieval but cannot override these checks. Available answer types are `exact_code`, `exact_entity`, `number`, `date`, `set`, `instruction`, `status`, and `quote`.

Numbers retain displayed thresholds/percentages and normalize Bengali digits and grouping separators. Dates currently require ISO format. Status extraction currently supports narrow explicit English stock/compatibility statements. Instructions are exact paragraphs or complete bounded list sequences; this version does not claim general semantic understanding or paraphrase equivalence in Bangla. `position` selects within a named HTML list; a tiled historical screenshot alone does not establish the ordinal identity of a logo.

`scope: "page"` excludes API/embedded JSON answers. `scope: "data"` selects those records, whose visibility remains unverified. `scope: "all_sources"` can expose contradictory values. `compare_to: "snapshot:..."` compares the same typed query against another registered observation. Different values with known matching URLs and different times are labeled `temporal_difference`; missing alignment information produces `unresolved_reference`. Neither status silently replaces one reference with the other or proves a causal change.

`as_of: "current"` refuses historical snapshots as evidence of current state and is checked again at final answer verification. An explicit timestamp requires a matching capture timestamp. For live use, the server administrator must set `LWA_V2_ALLOW_LIVE=1`; then `source` may be `{"kind":"live","url":"https://example.org","render":"auto"}`. Auto mode starts with HTTP and makes at most one browser escalation if unresolved, or scripts/styles leave rendered visibility uncertain, and time remains. `render: "browser"` captures rendered DOM, geometry, bounded screenshot pixels, and up to eight passive JSON responses. Initial rendering is not proof that every lazy or interactive state was reached.

## MCP client configuration

Launch the server with the same Python environment and store used for registration. A standard stdio client configuration is:

```json
{
  "mcpServers": {
    "lwa-v2": {
      "command": "/absolute/path/to/repository/.venv-lwa-v2/bin/python",
      "args": ["/absolute/path/to/repository/scripts/mcp_evidence_gateway.py"],
      "env": {
        "LWA_V2_STORE": "/absolute/path/to/private-v2-store",
        "LWA_V2_ALLOW_LIVE": "0",
        "LWA_V2_MAX_CALLS": "40"
      }
    }
  }
}
```

The MCP request schema is generated from [`schemas.py`](../scripts/evidence_gateway/schemas.py). Do not expose the legacy path-based tools alongside v2 in a supposedly isolated offline evaluation. A stdio server process has one trusted session identity by default. Set `LWA_V2_SESSION_ID` in the host environment to retain its call budget across process restarts; agents cannot supply or reset this identity through the tools. Restarting without a fixed host identity starts a new session.

## Visual evidence and optional vision adapter

The compiler indexes source regions and browser geometry. The resolver selects regions using labels or one cached overview OCR pass, then runs bounded detailed OCR. `inspect_evidence` with `view: "crop"` returns an actual MCP image block with source hash and original coordinates. There is no image/base64 payload in a normal resolution certificate.

Two Tesseract layout modes are correlated readings from one engine. Their agreement is labeled `corroborated_visual`, not `supported`. The uncalibrated minimum word-confidence filter defaults to 80; change it with `LWA_V2_MIN_OCR_CONFIDENCE` and evaluate the error/abstention tradeoff. By default the final answer gate rejects visual-only certificates. `LWA_V2_ALLOW_VISUAL_ANSWERS=1` allows corroborated visual answers with their evidence status retained. It never allows an ambiguous certificate.

For optional stronger visual reading, a trusted host can set:

- `LWA_V2_VISION_COMMAND`: a JSON argv array naming its adapter executable. No shell interpolation is used.
- `LWA_V2_VISION_ID`: an explicit model/configuration version. Update it when model or prompting changes.
- Request budget `max_vision_calls: 1`.

The adapter reads one JSON object from stdin containing `image_png_base64`, a transcription `instruction`, and `model_id`. It writes JSON containing `text`, the matching `model_id`, and optionally provider-reported `usage`. Output is capped at 32 KB; one bounded crop is supplied. The response is cached by crop hash/coordinates and runtime identity. An adapter failure or disagreement remains unresolved. The implementation tests use a local fixture adapter; no paid vision provider is configured by default.

## Limits and measurement

Resolution has a server-side process deadline, including acquisition, indexing, OCR, and any vision subprocess. On expiry, its process group is terminated and the caller receives `coverage_incomplete`. Each actual MCP entry consumes a session call, including inspections and verification, independent of outer Code Mode calls. Image inspection is limited to one million returned pixels per call and eight million per session. Source images are capped at eight MB and 80 million pixels. HTTP/DOM storage is capped at four MB; certificates at 6,000 UTF-8 bytes. Browser screenshots stop at 6,000 pixels high; request count is bounded, but total browser network-transfer bytes are not a hard aggregate cap.

The 600–900-token figure in the architecture is a target, not an enforced tokenizer-independent limit. Set `LWA_V2_TOKENIZER` to an installed tiktoken encoding name to count the exact certificate under that encoding. Such a count is not the total agent context, image tokens, or provider billing, and a different model tokenizer may count differently. Actual host model usage can be attached with `Gateway.record_model_usage()`; it is recorded explicitly as host-reported. The SQLite audit also records timings, cache hits, OCR/vision invocations, and inspection bytes. Cache-cold and warm performance must be reported separately.

Content hashes verify blobs and immutable records when read. This store is a private local cache, not a cryptographic attestation service against a malicious administrator. Parser, OCR, and perception errors remain possible. A matched agent evaluation is still needed before claiming improved accuracy or end-to-end token savings over v1.
