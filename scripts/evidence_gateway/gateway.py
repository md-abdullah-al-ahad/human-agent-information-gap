"""Resolver, persistent answer gate, and process-enforced request budgets."""

from __future__ import annotations

import json
import os
import re
import secrets
import signal
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

from . import VERSION
from .acquisition import acquire_browser, acquire_http
from .compiler import compile_capture, crop_pixels
from .protocol import (
    bound_to_question,
    extract_values,
    ranked_records,
    stale_reason,
    validate_request,
)
from .store import Store, digest, encode
from .visual import runtime_identity, visual_evidence

MAX_CERT_BYTES = 6000
MAX_INSPECT_CHARS = 1600


def compact_evidence(record):
    value = {
        "id": record["id"],
        "source_kind": record["source_kind"],
        "source_sha256": record["source_sha256"],
        "locator": record.get("locator"),
        "human_visibility": record.get("human_visibility", "unverified"),
        "text": record.get("text", "")[:180],
    }
    if record.get("bbox"):
        value["bbox"] = record["bbox"]
    if record.get("method"):
        value["method"] = record["method"]
    return value


def certificate(
    store,
    query,
    event,
    status,
    reason,
    value=None,
    evidence=(),
    candidates=(),
    checks=(),
    coverage=(),
    comparison=None,
):
    payload = {
        "version": VERSION,
        "capture_id": event.get("capture_id"),
        "snapshot_id": query["source"].get("id"),
        "captured_at": event.get("captured_at"),
        "status": status,
        "answer_type": query["answer_type"],
        "value": value,
        "interpretation": {
            k: query[k]
            for k in ("subject", "field", "qualifiers", "scope", "as_of", "position")
        },
        "evidence": [compact_evidence(r) for r in evidence[:3]],
        "candidates": list(candidates)[:3],
        "reason": reason,
        "checks": list(checks),
        "coverage": sorted(set(coverage)),
        "next_action": None,
    }
    if comparison:
        payload["comparison"] = comparison
    if len(candidates) > 3:
        payload["additional_candidate_count"] = len(candidates) - 3
    if status not in {"supported", "corroborated_visual"} and payload["evidence"]:
        payload["next_action"] = {
            "tool": "inspect_evidence",
            "evidence_id": payload["evidence"][0]["id"],
            "view": "crop" if payload["evidence"][0].get("bbox") else "text",
        }
    # Reserve the final handle length; never truncate a supported answer silently.
    if len(encode(payload)) + 100 > MAX_CERT_BYTES:
        payload.update(
            status="coverage_incomplete",
            value=None,
            candidates=[],
            reason="The exact answer exceeds the compact response budget; inspect the source.",
        )
        for record in payload["evidence"]:
            record["text"] = record["text"][:80]
    if len(encode(payload)) + 100 > MAX_CERT_BYTES:
        for record in payload["evidence"]:
            record["text"] = ""
        if comparison:
            payload["comparison"] = [
                {k: v for k, v in item.items() if k != "value"} for item in comparison
            ]
    if len(encode(payload)) + 100 > MAX_CERT_BYTES:
        raise ValueError("request interpretation exceeds the certificate byte budget")
    handle = store.put("cert", payload)
    return dict(payload, certificate_id=handle)


def resolve_worker(store, query):
    started = time.monotonic()
    deadline = started + query["budget"]["max_wall_ms"] / 1000
    source = query["source"]
    live_auto = source["kind"] == "live" and source.get("render", "auto") == "auto"
    if source["kind"] == "live":
        if os.environ.get("LWA_V2_ALLOW_LIVE") != "1":
            raise ValueError("live acquisition is disabled by the server")
        acquire = acquire_browser if source.get("render") == "browser" else acquire_http
        try:
            registered = acquire(store, source, max(0.1, deadline - time.monotonic()))
        except Exception as error:  # noqa: BLE001 -- acquisition errors are explicit evidence states
            return {
                "certificate": certificate(
                    store,
                    query,
                    {},
                    "coverage_incomplete",
                    "Acquisition failed: " + type(error).__name__,
                    coverage=["access_failed"],
                ),
                "usage": {"acquisition_failed": True},
            }
        query = dict(
            query, source={"kind": "snapshot", "id": registered["snapshot_id"]}
        )
    event = store.get(query["source"]["id"], "snapshot")
    capture_id = event["capture_id"]
    runtime = runtime_identity()
    versions = {name: version(name) for name in ("beautifulsoup4", "Pillow")}
    cache_key = "query:" + digest(
        encode(
            [
                query,
                runtime,
                versions,
                VERSION,
                os.environ.get("LWA_V2_MIN_OCR_CONFIDENCE", "80"),
            ]
        )
    )
    stale = stale_reason(query, event)
    if stale:
        return {
            "certificate": certificate(
                store, query, event, "stale", stale, coverage=event["coverage"]
            ),
            "usage": {"query_cache_hit": False},
        }
    cached = store.cached(cache_key) if query["as_of"] != "current" else None
    if cached:
        return {
            "certificate": dict(store.get(cached, "cert"), certificate_id=cached),
            "usage": {"query_cache_hit": True},
        }
    index, index_hit = compile_capture(store, capture_id)
    coverage = index["coverage"] + event["coverage"]
    usage = {
        "query_cache_hit": False,
        "index_cache_hit": index_hit,
        "indexed_records": len(index["records"]),
        "source_html_bytes": index["html_bytes"],
        "source_image_bytes": index["image_bytes"],
    }
    if index["blocked"] or event.get("http_status") in {401, 403, 429}:
        answer = certificate(
            store,
            query,
            event,
            "access_blocked",
            "The captured response is an access challenge or denial.",
            coverage=coverage,
        )
    elif event.get("http_status") and event["http_status"] >= 400:
        answer = certificate(
            store,
            query,
            event,
            "coverage_incomplete",
            "The HTTP request failed.",
            coverage=coverage,
        )
    else:
        records = list(index["records"])
        for handle in query["evidence_ids"]:
            record = store.get(handle, "ev")
            if record["capture_id"] != capture_id:
                raise ValueError("evidence does not belong to the requested capture")
            if not any(r["id"] == handle for r in records):
                records.append(dict(record, id=handle))
        ranked = ranked_records(records, query)
        pairs = []
        for record in ranked:
            if record["source_kind"] in {
                "image_region",
                "visual_reading",
            } or not bound_to_question(record, query):
                continue
            if (
                query["answer_type"] in {"instruction", "set"}
                and record.get("sequence")
                and query["position"] is None
            ):
                continue
            values = (
                record.get("items")
                if query["answer_type"] in {"instruction", "set"}
                and record.get("items")
                else extract_values(record, query)
            )
            if record.get("items") and query["answer_type"] in {"instruction", "set"}:
                pairs.append((values, record))
            else:
                pairs.extend((v, record) for v in values)
        visual_records, selected, failures = [], [], []
        if not pairs or query["evidence_ids"]:
            visual_records, selected, failures, visual_usage = visual_evidence(
                store, index, query, runtime, lambda: deadline - time.monotonic()
            )
            usage.update(visual_usage)
            for record in visual_records:
                if bound_to_question(record, query):
                    pairs.extend((v, record) for v in extract_values(record, query))
        distinct = {}
        for value, record in pairs:
            distinct.setdefault(encode(value).decode(), (value, []))[1].append(record)
        if len(distinct) > 1:
            supporting = [r for _, rows in distinct.values() for r in rows]
            modalities = {r["source_kind"] for r in supporting}
            status = (
                "source_conflict"
                if "network_json" in modalities or "embedded_json" in modalities
                else "ambiguous"
            )
            answer = certificate(
                store,
                query,
                event,
                status,
                "Bound source readings disagree; an exact value was not selected.",
                evidence=supporting,
                candidates=[v for v, _ in distinct.values()],
                coverage=coverage,
            )
        elif distinct:
            value, supporting = next(iter(distinct.values()))
            text_records = [
                r for r in supporting if r["source_kind"] != "visual_reading"
            ]
            if text_records:
                answer = certificate(
                    store,
                    query,
                    event,
                    "supported",
                    "Exact extraction from a subject-bound captured source.",
                    value,
                    evidence=text_records,
                    checks=["subject_bound", "qualifiers_bound", "typed_extraction"],
                    coverage=coverage,
                )
            else:
                # Corroboration requires distinct methods on the same selected region.
                groups = {}
                minimum = float(os.environ.get("LWA_V2_MIN_OCR_CONFIDENCE", "80"))
                for r in supporting:
                    if (
                        r.get("min_confidence") is not None
                        and r["min_confidence"] < minimum
                    ):
                        continue
                    groups.setdefault((r["source_sha256"], r["region_id"]), set()).add(
                        r["method"]
                    )
                agreement = any(len(methods) >= 2 for methods in groups.values())
                answer = certificate(
                    store,
                    query,
                    event,
                    "corroborated_visual" if agreement else "ambiguous",
                    "Visual readings agree; perception remains fallible."
                    if agreement
                    else "An exact visual reading lacks corroboration.",
                    value if agreement else None,
                    evidence=supporting,
                    candidates=[] if agreement else [value],
                    checks=["subject_bound", "same_region_readings"]
                    if agreement
                    else [],
                    coverage=coverage + failures,
                )
        else:
            available = selected or ranked[:3]
            answer = certificate(
                store,
                query,
                event,
                "coverage_incomplete"
                if selected or failures
                else "not_observed_in_scope",
                "No subject-bound value passed the typed checks in the inspected scope. This is not proof of absence.",
                evidence=available,
                coverage=coverage + failures,
            )
    needs_browser = answer["status"] in {
        "not_observed_in_scope",
        "coverage_incomplete",
    } or (
        answer["status"] == "supported"
        and index.get("requires_render")
        and query["scope"] == "page"
    )
    if live_auto and needs_browser and deadline - time.monotonic() > 2:
        try:
            rendered = acquire_browser(store, source, deadline - time.monotonic())
            followup = dict(
                query,
                source={"kind": "snapshot", "id": rendered["snapshot_id"]},
                budget=dict(
                    query["budget"],
                    max_wall_ms=max(100, int((deadline - time.monotonic()) * 1000)),
                ),
            )
            result = resolve_worker(store, followup)
            result["usage"]["http_before_browser"] = usage
            result["usage"]["browser_escalated"] = True
            return result
        except Exception as error:  # noqa: BLE001 -- preserve an unresolved acquisition rather than certify initial HTML
            usage["browser_escalation_error"] = type(error).__name__
            records = [
                dict(store.get(e["id"], "ev"), id=e["id"]) for e in answer["evidence"]
            ]
            answer = certificate(
                store,
                query,
                event,
                "coverage_incomplete",
                "Browser escalation failed; rendered evidence remains unverified.",
                evidence=records,
                coverage=coverage + ["browser_escalation_failed"],
            )
    if query.get("compare_to") and answer["status"] not in {"access_blocked", "stale"}:
        other_query = dict(
            query,
            source={"kind": "snapshot", "id": query["compare_to"]},
            compare_to=None,
            evidence_ids=[],
            as_of="capture",
            budget=dict(
                query["budget"],
                max_wall_ms=max(100, int((deadline - time.monotonic()) * 1000)),
            ),
        )
        other_result = resolve_worker(store, other_query)
        other = other_result["certificate"]
        other_event = store.get(query["compare_to"], "snapshot")
        comparison = [
            {
                "snapshot_id": c["snapshot_id"],
                "captured_at": c["captured_at"],
                "status": c["status"],
                "value": c["value"],
            }
            for c in (answer, other)
        ]
        if (
            answer["status"] == other["status"] == "supported"
            and answer["value"] == other["value"]
        ):
            reason, status, value = (
                "Both saved observations support the same extracted value.",
                "supported",
                answer["value"],
            )
        else:
            aligned_url = event.get("requested_url") and event.get(
                "requested_url"
            ) == other_event.get("requested_url")
            both_supported = answer["status"] == other["status"] == "supported"
            if (
                aligned_url
                and both_supported
                and event.get("captured_at")
                and other_event.get("captured_at")
            ):
                status = (
                    "temporal_difference"
                    if event["captured_at"] != other_event["captured_at"]
                    else "source_conflict"
                )
                reason = "The same query has differing saved observations; capture times are shown and neither reference is silently substituted."
            else:
                status, reason = (
                    "unresolved_reference",
                    "The reference cannot be fully aligned or resolved; this does not establish temporal change.",
                )
            value = None
        records = [
            dict(store.get(e["id"], "ev"), id=e["id"])
            for c in (answer, other)
            for e in c["evidence"]
        ]
        answer = certificate(
            store,
            query,
            event,
            status,
            reason,
            value=value,
            evidence=records,
            comparison=comparison,
            coverage=coverage,
        )
        usage["reference_usage"] = other_result["usage"]
    usage["worker_ms"] = round((time.monotonic() - started) * 1000, 2)
    # Missing runtime and partial time-bound results are not permanent query-cache answers.
    if query["as_of"] != "current" and answer["status"] in {
        "supported",
        "corroborated_visual",
        "access_blocked",
        "source_conflict",
        "ambiguous",
    }:
        store.cache(cache_key, answer["certificate_id"])
    return {"certificate": answer, "usage": usage}


class Gateway:
    def __init__(self, root=None, session_id=None, max_calls=None, allow_visual=None):
        self.store = Store(root)
        self.session_id = (
            session_id or os.environ.get("LWA_V2_SESSION_ID") or secrets.token_hex(16)
        )
        self.max_calls = int(max_calls or os.environ.get("LWA_V2_MAX_CALLS", "40"))
        self.allow_visual = (
            os.environ.get("LWA_V2_ALLOW_VISUAL_ANSWERS") == "1"
            if allow_visual is None
            else allow_visual
        )

    def _charge(self, pixels=0):
        self.store.charge(self.session_id, self.max_calls, pixels)

    def resolve(self, request):
        query = validate_request(request)
        self._charge()
        if (
            query["source"]["kind"] == "live"
            and os.environ.get("LWA_V2_ALLOW_LIVE") != "1"
        ):
            raise ValueError("live acquisition is disabled by the server")
        # Validate the registered handle before starting a subprocess; paths are never accepted.
        if query["source"]["kind"] == "snapshot":
            self.store.get(query["source"]["id"], "snapshot")
        started = time.monotonic()
        worker = Path(__file__).resolve().parents[1] / "evidence_gateway_cli.py"
        process = subprocess.Popen(
            [sys.executable, str(worker), "--store", str(self.store.root), "_worker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(
                encode(query), timeout=query["budget"]["max_wall_ms"] / 1000
            )
            if process.returncode:
                raise RuntimeError(
                    "Evidence worker failed: " + stderr.decode(errors="replace")[-300:]
                )
            result = json.loads(stdout)
            if "error" in result:
                raise ValueError(result["error"])
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            event = (
                self.store.get(query["source"]["id"], "snapshot")
                if query["source"]["kind"] == "snapshot"
                else {}
            )
            result = {
                "certificate": certificate(
                    self.store,
                    query,
                    event,
                    "coverage_incomplete",
                    "The server wall-time budget expired; unfinished processing was terminated.",
                    coverage=["processing_budget_exhausted"],
                ),
                "usage": {"timed_out": True},
            }
        result["usage"]["certificate_bytes"] = len(encode(result["certificate"]))
        encoding = os.environ.get("LWA_V2_TOKENIZER")
        if encoding:
            result["usage"]["tokenizer"] = encoding
            remaining = query["budget"]["max_wall_ms"] / 1000 - (
                time.monotonic() - started
            )
            try:
                counter = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "import sys,tiktoken; print(len(tiktoken.get_encoding(sys.argv[1]).encode(sys.stdin.read(), disallowed_special=())))",
                        encoding,
                    ],
                    input=encode(result["certificate"]),
                    capture_output=True,
                    timeout=max(0.01, min(2, remaining)),
                    check=True,
                )
                result["usage"]["certificate_tokens"] = int(counter.stdout)
            except (
                subprocess.TimeoutExpired,
                subprocess.CalledProcessError,
                ValueError,
            ):
                result["usage"]["certificate_tokens"] = None
                result["usage"]["tokenizer_status"] = "unavailable_within_budget"
        result["usage"]["elapsed_ms"] = round((time.monotonic() - started) * 1000, 2)
        self.store.audit(
            self.session_id,
            "resolve",
            {
                "certificate_id": result["certificate"]["certificate_id"],
                **result["usage"],
            },
        )
        return result

    def inspect(self, evidence_id, view="text"):
        if view not in {"text", "crop"}:
            raise ValueError("view must be text or crop")
        record = self.store.get(evidence_id, "ev")
        if view == "crop":
            if not record.get("bbox"):
                raise ValueError("evidence has no saved pixel region")
            b = record["bbox"]
            self._charge(min(1_000_000, (b[2] - b[0]) * (b[3] - b[1])))
            pixels, size = crop_pixels(self.store, record)
            metadata = {
                **compact_evidence(dict(record, id=evidence_id)),
                "returned_dimensions": size,
                "crop_sha256": digest(pixels),
            }
            self.store.audit(
                self.session_id,
                "inspect_crop",
                {
                    "evidence_id": evidence_id,
                    "pixel_dimensions": size,
                    "bytes": len(pixels),
                },
            )
            return metadata, pixels
        self._charge()
        source_bytes = self.store.read_blob(record["source_sha256"])
        # Full runtime/index metadata stays in the store; return bounded exact source text.
        result = compact_evidence(dict(record, id=evidence_id))
        result["text"] = record.get("text", "")[:MAX_INSPECT_CHARS]
        result["truncated"] = len(record.get("text", "")) > MAX_INSPECT_CHARS
        result["human_visibility"] = record.get("human_visibility")
        location = re.fullmatch(r"html:(\d+):(\d+)", record.get("locator") or "")
        if location:
            lines = source_bytes.decode("utf-8", errors="replace").splitlines()
            line, column = map(int, location.groups())
            if 0 < line <= len(lines):
                result["source_excerpt"] = lines[line - 1][
                    max(0, column - 40) : column + 360
                ]
        if record.get("items"):
            result["items"] = []
            available = MAX_INSPECT_CHARS
            for item in record["items"][:12]:
                if not available:
                    break
                snippet = item[: min(400, available)]
                result["items"].append(snippet)
                available -= len(snippet)
            result["truncated"] |= result["items"] != record["items"]
        self.store.audit(self.session_id, "inspect_text", {"evidence_id": evidence_id})
        return result, None

    def verify(self, certificate_id, proposed_answer):
        self._charge()
        cert = self.store.get(certificate_id, "cert")
        if not isinstance(proposed_answer, dict) or set(proposed_answer) != {
            "value",
            "evidence_ids",
        }:
            raise ValueError(
                "proposed_answer must contain only value and evidence_ids; free prose is not an exact answer"
            )
        allowed = cert["status"] == "supported" or (
            cert["status"] == "corroborated_visual" and self.allow_visual
        )
        required = sorted({e["id"] for e in cert["evidence"]})
        ids = proposed_answer["evidence_ids"]
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            raise ValueError("evidence_ids must be a list of handles")
        reason = None
        if not allowed:
            reason = "certificate_status_not_allowed"
        elif cert["interpretation"]["as_of"] == "current" and stale_reason(
            cert["interpretation"], self.store.get(cert["snapshot_id"], "snapshot")
        ):
            reason = "certificate_stale_at_verification"
        elif encode(proposed_answer["value"]) != encode(cert["value"]):
            reason = "exact_value_or_required_steps_mismatch"
        elif sorted(set(ids)) != required:
            reason = "evidence_citations_mismatch"
        result = {
            "status": "rejected" if reason else "accepted",
            "certificate_id": certificate_id,
            "reason": reason,
        }
        if not reason:
            for evidence in cert["evidence"]:
                self.store.read_blob(evidence["source_sha256"])
            # This is the host adapter's final artifact. No unchecked agent prose is copied.
            result["answer"] = {
                "value": cert["value"],
                "evidence_ids": required,
                "evidence_status": cert["status"],
                "captured_at": cert["captured_at"],
            }
        self.store.audit(self.session_id, "verify", result)
        return result

    def answer(self, request):
        """Enforced host path: construct the final response exclusively from a certificate."""
        result = self.resolve(request)
        cert = result["certificate"]
        result["gate"] = self.verify(
            cert["certificate_id"],
            {
                "value": cert["value"],
                "evidence_ids": [e["id"] for e in cert["evidence"]],
            },
        )
        return result

    def record_model_usage(
        self,
        certificate_id,
        *,
        provider,
        model,
        input_tokens,
        output_tokens,
        image_tokens=None,
        reported_cost=None,
    ):
        """Trusted host telemetry hook; deliberately not an agent-facing MCP tool."""
        self.store.get(certificate_id, "cert")
        for count in (input_tokens, output_tokens, image_tokens):
            if count is not None and (type(count) is not int or count < 0):
                raise ValueError("token counts must be nonnegative integers or unknown")
        if reported_cost is not None and (
            type(reported_cost) not in {float, int} or reported_cost < 0
        ):
            raise ValueError("reported_cost must be nonnegative or unknown")
        self.store.audit(
            self.session_id,
            "host_model_usage",
            {
                "certificate_id": certificate_id,
                "provider": provider,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "image_tokens": image_tokens,
                "reported_cost": reported_cost,
                "attribution": "host_reported_not_independently_reconciled",
            },
        )
