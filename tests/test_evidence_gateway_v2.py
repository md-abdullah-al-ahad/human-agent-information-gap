"""Contract and integration tests; no paid agent runs or live-site experiments."""

import io
import json
import os
import tempfile
import time
import unittest
from datetime import UTC
from pathlib import Path
from unittest.mock import patch

from scripts.evidence_gateway.compiler import compile_capture
from scripts.evidence_gateway.gateway import MAX_CERT_BYTES, Gateway, resolve_worker
from scripts.evidence_gateway.protocol import validate_request
from scripts.evidence_gateway.store import Store, encode


class GatewayFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(self.root / "store")
        self.gateway = Gateway(self.store.root, max_calls=100)
        self.env = patch.dict(
            os.environ,
            {
                "LWA_V2_ALLOW_LIVE": "0",
                "LWA_V2_TESSERACT": "/nonexistent/tesseract",
                "LWA_V2_VISION_COMMAND": "",
                "LWA_V2_VISION_ID": "",
                "LWA_V2_TOKENIZER": "",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)

    def register(self, html, **kwargs):
        return self.store.ingest(html.encode(), **kwargs)["snapshot_id"]

    def request(self, snapshot, **kwargs):
        return {
            "source": {"kind": "snapshot", "id": snapshot},
            "question": "What is the offer code?",
            "subject": "Travel offer",
            "answer_type": "exact_code",
            **kwargs,
        }

    def resolve(self, snapshot, **kwargs):
        return self.gateway.resolve(self.request(snapshot, **kwargs))["certificate"]


class GatewayTests(GatewayFixture):
    def test_content_identity_deduplicates_acquisitions_but_preserves_times(self):
        first = self.store.ingest(
            b"<p>Same page</p>", captured_at="2026-01-01T00:00:00Z"
        )
        second = self.store.ingest(
            b"<p>Same page</p>", captured_at="2026-02-01T00:00:00Z"
        )
        self.assertEqual(first["capture_id"], second["capture_id"])
        self.assertNotEqual(first["snapshot_id"], second["snapshot_id"])
        self.assertNotEqual(first["captured_at"], second["captured_at"])
        self.assertEqual(len(list((self.store.root / "blobs").glob("*/*"))), 1)

    def test_registration_copies_sources_and_rejects_outside_and_symlink(self):
        allowed = self.root / "packet"
        allowed.mkdir()
        page = allowed / "page.html"
        page.write_text("<p>Travel offer code: AIRN10</p>")
        registered = self.store.register(allowed, "page.html")
        page.write_text("<p>Changed page</p>")
        self.assertEqual(self.resolve(registered["snapshot_id"])["value"], "AIRN10")
        outside = self.root / "secret.html"
        outside.write_text("private")
        (allowed / "escape.html").symlink_to(outside)
        for path in (outside, "escape.html", "../secret.html"):
            with self.assertRaises(ValueError):
                self.store.register(allowed, path)

    def test_agent_request_cannot_supply_paths_or_enable_live(self):
        with self.assertRaises(ValueError):
            self.gateway.resolve(self.request("/etc/passwd"))
        with self.assertRaises(ValueError):
            self.gateway.resolve(
                self.request("snapshot:" + "0" * 64, path="/etc/passwd")
            )
        with self.assertRaises(ValueError):
            self.gateway.resolve(
                {
                    "source": {"kind": "live", "url": "https://example.org"},
                    "subject": "Travel",
                    "answer_type": "quote",
                }
            )

    def test_replay_certificate_and_different_question_reuse_index(self):
        snapshot = self.register("<article>Travel offer code: AIRN10</article>")
        request = self.request(snapshot)
        first = self.gateway.resolve(request)
        second = self.gateway.resolve(request)
        self.assertEqual(first["certificate"], second["certificate"])
        self.assertFalse(first["usage"]["index_cache_hit"])
        self.assertTrue(second["usage"]["query_cache_hit"])
        third = self.gateway.resolve(
            self.request(snapshot, question="Tell me the code")
        )
        self.assertTrue(third["usage"]["index_cache_hit"])
        self.assertEqual(
            first["certificate"]["evidence"], third["certificate"]["evidence"]
        )

    def test_coupon_binding_and_exact_gate(self):
        snapshot = self.register(
            "<section><article><h2>Travel offer 7%</h2><p>Code: AIRN10</p></article>"
            "<article><h2>Travel offer 9%</h2><p>Code: AIRR10</p></article></section>"
        )
        cert = self.resolve(snapshot, qualifiers={"discount": "7%"})
        self.assertEqual(cert["status"], "supported")
        self.assertEqual(cert["value"], "AIRN10")
        proposal = {
            "value": "AIRN10",
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        self.assertEqual(
            self.gateway.verify(cert["certificate_id"], proposal)["status"], "accepted"
        )
        proposal["value"] = "AIRR10"
        self.assertEqual(
            self.gateway.verify(cert["certificate_id"], proposal)["reason"],
            "exact_value_or_required_steps_mismatch",
        )

    def test_competing_same_subject_codes_are_ambiguous(self):
        snapshot = self.register(
            "<article>Travel offer Code: ABCN10</article><article>Travel offer Code: ABCR10</article>"
        )
        cert = self.resolve(snapshot)
        self.assertEqual(cert["status"], "ambiguous")
        self.assertIsNone(cert["value"])
        self.assertEqual(set(cert["candidates"]), {"ABCN10", "ABCR10"})

    def test_wrong_card_and_percentage_substring_do_not_bind(self):
        snapshot = self.register(
            "<article>Travel offer 17% Code: ABCN10</article><article>Local offer 7% Code: ABCR10</article>"
        )
        cert = self.resolve(snapshot, qualifiers={"discount": "7%"})
        self.assertIsNone(cert["value"])
        self.assertEqual(cert["status"], "not_observed_in_scope")

    def test_names_preserve_script_and_require_exact_value(self):
        snapshot = self.register(
            "<article>Parent testimonial <p>Name: সুমনা দাস</p></article>"
        )
        cert = self.resolve(
            snapshot,
            subject="Parent testimonial",
            answer_type="exact_entity",
            field="Name",
        )
        self.assertEqual(cert["value"], "সুমনা দাস")
        self.assertEqual(
            self.gateway.verify(
                cert["certificate_id"],
                {
                    "value": "সুমনা দেবী",
                    "evidence_ids": [e["id"] for e in cert["evidence"]],
                },
            )["status"],
            "rejected",
        )

    def test_instruction_sequence_cannot_drop_a_step(self):
        snapshot = self.register(
            "<section><h2>Oil preparation</h2><ol><li>Strain the oil.</li><li>Use it in curry.</li></ol></section>"
        )
        cert = self.resolve(
            snapshot, subject="Oil preparation", answer_type="instruction"
        )
        self.assertEqual(cert["status"], "supported")
        self.assertEqual(cert["value"], ["Strain the oil.", "Use it in curry."])
        proposal = {
            "value": ["Use it in curry."],
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        self.assertEqual(
            self.gateway.verify(cert["certificate_id"], proposal)["status"], "rejected"
        )

    def test_position_resolves_within_named_list(self):
        snapshot = self.register(
            "<section><h2>Partner brands</h2><ol><li>Brand: Alpha</li><li>Brand: Beta</li></ol></section>"
        )
        cert = self.resolve(
            snapshot,
            subject="Partner brands",
            answer_type="exact_entity",
            field="Brand",
            position=2,
        )
        self.assertEqual(cert["value"], "Beta")

    def test_no_stock_from_button_or_another_subject(self):
        for html in (
            "<article>Blue model <button>Buy Now</button></article>",
            "<article>Blue model; Red model is in stock</article>",
            "<p>Blue model might be in stock</p>",
        ):
            cert = self.resolve(
                self.register(html), subject="Blue model", answer_type="status"
            )
            self.assertIsNone(cert["value"])
        cert = self.resolve(
            self.register("<p>Blue model is out of stock</p>"),
            subject="Blue model",
            answer_type="status",
        )
        self.assertEqual(cert["value"], "out_of_stock")

    def test_data_stays_separate_and_conflict_is_explicit(self):
        snapshot = self.register(
            "<article>Blue model <p>Price: 20</p></article>"
            '<script type="application/ld+json">{"name":"Blue model","price":25}</script>'
        )
        page = self.resolve(
            snapshot, subject="Blue model", answer_type="number", field="Price"
        )
        self.assertEqual(page["value"], "20")
        all_sources = self.resolve(
            snapshot,
            subject="Blue model",
            answer_type="number",
            field="Price",
            scope="all_sources",
        )
        self.assertEqual(all_sources["status"], "source_conflict")
        self.assertEqual(set(all_sources["candidates"]), {"20", "25"})
        data = self.resolve(
            snapshot,
            subject="Blue model",
            answer_type="number",
            field="Price",
            scope="data",
        )
        self.assertEqual(data["value"], "25")
        self.assertEqual(data["evidence"][0]["source_kind"], "embedded_json")

    def test_bangla_number_normalization_and_date_ambiguity(self):
        snapshot = self.register(
            "<article>App statistics <p>Downloads: ৫,০০,০০০+</p><p>Date: 03/04/2026</p></article>"
        )
        cert = self.resolve(
            snapshot, subject="App statistics", answer_type="number", field="Downloads"
        )
        self.assertEqual(cert["value"], "500000+")
        cert = self.resolve(
            snapshot, subject="App statistics", answer_type="date", field="Date"
        )
        self.assertIsNone(cert["value"])

    def test_current_query_does_not_reuse_historical_answer(self):
        snapshot = self.register(
            "<p>Travel offer Code: ABCN10</p>", captured_at="2026-01-01T00:00:00Z"
        )
        self.assertEqual(self.resolve(snapshot)["value"], "ABCN10")
        self.assertEqual(self.resolve(snapshot, as_of="current")["status"], "stale")
        unknown = self.register("<p>Travel offer Code: ABCN10</p>")
        self.assertEqual(
            self.resolve(unknown, as_of="2026-01-01T00:00:00Z")["status"], "stale"
        )

    def test_blocked_page_has_no_answer(self):
        cert = self.resolve(
            self.register("<h1>Verify you are human</h1><p>Travel offer ABCN10</p>")
        )
        self.assertEqual(cert["status"], "access_blocked")
        self.assertEqual(cert["evidence"], [])

    def test_hidden_nodes_do_not_supply_answers(self):
        snapshot = self.register(
            "<article hidden>Travel offer Code: HIDE10</article><article>Travel offer Code: SHOW10</article>"
        )
        self.assertEqual(self.resolve(snapshot)["value"], "SHOW10")

    def test_image_crop_and_no_filename_answer(self):
        from PIL import Image

        image = Image.new("RGB", (12, 10), "red")
        image.putpixel((3, 4), (0, 0, 255))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        registered = self.store.ingest(
            b"<p>Travel offer</p>",
            [{"bytes": buffer.getvalue(), "role": "saved_image"}],
        )
        cert = self.resolve(registered["snapshot_id"], budget={"max_ocr_calls": 0})
        self.assertIsNone(cert["value"])
        ev = cert["evidence"][0]["id"]
        metadata, pixels = self.gateway.inspect(ev, "crop")
        self.assertEqual(metadata["bbox"], [0, 0, 12, 10])
        self.assertEqual(Image.open(io.BytesIO(pixels)).getpixel((3, 4)), (0, 0, 255))

    def test_source_integrity_and_cross_capture_evidence(self):
        first = self.resolve(self.register("<p>Travel offer code: FIRST10</p>"))
        other = self.register("<p>Travel offer code: OTHER10</p>")
        with self.assertRaises(ValueError):
            self.resolve(other, evidence_ids=[first["evidence"][0]["id"]])
        sha = first["evidence"][0]["source_sha256"]
        (self.store.root / "blobs" / sha[:2] / sha).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            self.store.read_blob(sha)

    def test_gate_rejects_added_prose_and_wrong_citations(self):
        cert = self.resolve(self.register("<p>Travel offer Code: EXACT10</p>"))
        with self.assertRaises(ValueError):
            self.gateway.verify(
                cert["certificate_id"],
                {
                    "value": "EXACT10",
                    "evidence_ids": [],
                    "explanation": "Also in stock",
                },
            )
        self.assertEqual(
            self.gateway.verify(
                cert["certificate_id"], {"value": "EXACT10", "evidence_ids": []}
            )["reason"],
            "evidence_citations_mismatch",
        )

    def test_call_budget_is_persistent_and_counts_actual_tool_entries(self):
        small = Gateway(self.store.root, session_id="fixed", max_calls=1)
        request = self.request(self.register("<p>Travel offer Code: EXACT10</p>"))
        small.resolve(request)
        with self.assertRaises(ValueError):
            Gateway(self.store.root, session_id="fixed", max_calls=1).resolve(request)

    def test_response_is_bounded_and_contains_no_page_dump(self):
        snapshot = self.register(
            "<article>Travel offer Code: EXACT10</article>"
            + "<p>unrelated content</p>" * 1000
        )
        result = self.gateway.resolve(self.request(snapshot))
        self.assertLessEqual(len(encode(result["certificate"])), MAX_CERT_BYTES)
        self.assertNotIn("unrelated content", encode(result).decode())
        self.assertLessEqual(len(result["certificate"]["evidence"]), 3)

    def test_host_adapter_only_emits_permitted_final_artifact(self):
        request = self.request(self.register("<p>Travel offer Code: EXACT10</p>"))
        result = self.gateway.answer(request)
        self.assertEqual(result["gate"]["answer"]["value"], "EXACT10")
        self.assertEqual(result["gate"]["status"], "accepted")

    def test_visual_disagreement_is_not_a_supported_code(self):
        from PIL import Image

        buffer = io.BytesIO()
        Image.new("RGB", (10, 10)).save(buffer, format="PNG")
        reg = self.store.ingest(b"<p>Travel offer</p>", [{"bytes": buffer.getvalue()}])
        index, _ = compile_capture(self.store, reg["capture_id"])
        region = next(r for r in index["records"] if r["source_kind"] == "image_region")
        readings = []
        for psm, code in ((6, "AIRN10"), (11, "AIRR10")):
            item = dict(
                region,
                source_kind="visual_reading",
                text=f"Travel offer Code: {code}",
                method=f"psm-{psm}",
                region_id=region["id"],
                min_confidence=95,
            )
            item.pop("id")
            readings.append(dict(item, id=self.store.put("ev", item)))
        with patch(
            "scripts.evidence_gateway.gateway.visual_evidence",
            return_value=(readings, [region], [], {}),
        ):
            result = resolve_worker(
                self.store, validate_request(self.request(reg["snapshot_id"]))
            )
        self.assertEqual(result["certificate"]["status"], "ambiguous")
        self.assertIsNone(result["certificate"]["value"])

    def test_visual_agreement_is_labeled_and_gate_defaults_to_reject(self):
        snapshot = self.register("<p>Travel offer</p>")
        event = self.store.get(snapshot)
        from scripts.evidence_gateway.gateway import certificate

        query = validate_request(self.request(snapshot))
        cert = certificate(
            self.store,
            query,
            event,
            "corroborated_visual",
            "Two readings agree",
            "VISUAL10",
        )
        self.assertEqual(
            self.gateway.verify(
                cert["certificate_id"], {"value": "VISUAL10", "evidence_ids": []}
            )["status"],
            "rejected",
        )

    def test_grounded_citation_substring_accepted_in_quote(self):
        snapshot = self.register(
            "<p>26 warehouses all over bangladesh 5 million orders have been delivered</p>"
        )
        cert = self.resolve(snapshot, subject="warehouses", answer_type="quote")
        proposal = {
            "value": "5 million",
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        result = self.gateway.verify(cert["certificate_id"], proposal)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["answer"]["value"], "5 million")

    def test_grounded_citation_ambiguous_set_accepted(self):
        snapshot = self.register(
            "<p>Currently Delivering in Dhaka Chittagong Sylhet</p>"
        )
        cert = self.resolve(snapshot, subject="Currently Delivering", answer_type="set")
        proposal = {
            "value": ["Dhaka", "Chittagong", "Sylhet"],
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        result = self.gateway.verify(cert["certificate_id"], proposal)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["answer"]["value"], ["Dhaka", "Chittagong", "Sylhet"])

    def test_cloudflare_challenge_detected_as_access_blocked_and_rejected_in_verify(self):
        snapshot = self.register(
            "<!DOCTYPE html><html><head><title>Just a moment...</title></head>"
            "<body><h2>Performing security verification</h2><p>Ray ID: 12345</p></body></html>"
        )
        cert = self.resolve(snapshot, subject="flight", answer_type="quote")
        self.assertEqual(cert["status"], "access_blocked")
        proposal = {
            "value": "Flight BG001",
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        result = self.gateway.verify(cert["certificate_id"], proposal)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["reason"], "access_blocked_cannot_answer")

    def test_visual_evidence_gate_honors_allow_visual_switch(self):
        snapshot = self.register("<p>Some page</p>")
        cert = self.resolve(snapshot, subject="Some page", answer_type="quote")
        blob_sha = self.store.blob(b"dummy_image_bytes")
        ev_id = self.store.put(
            "ev",
            {
                "capture_id": snapshot,
                "source_kind": "image_region",
                "source_sha256": blob_sha,
                "bbox": [0, 0, 100, 100],
                "text": "Promo Code: USBANG",
            },
        )
        proposal = {"value": "USBANG", "evidence_ids": [ev_id]}
        self.gateway.allow_visual = True
        self.assertEqual(
            self.gateway.verify(cert["certificate_id"], proposal)["status"], "accepted"
        )
        self.gateway.allow_visual = False
        self.assertEqual(
            self.gateway.verify(cert["certificate_id"], proposal)["status"], "rejected"
        )

    def test_field_number_without_colon_natural_extraction(self):
        snapshot = self.register(
            "<section><h2>Chaldal summary</h2><p>5 million orders have been delivered</p>"
            "<p>উপজেলা ৫০০ জেলা ৬৪</p></section>"
        )
        cert_orders = self.resolve(
            snapshot, subject="Chaldal summary", answer_type="number", field="orders"
        )
        self.assertEqual(cert_orders["status"], "supported")
        self.assertEqual(cert_orders["value"], "5")

        cert_upazila = self.resolve(
            snapshot, subject="Chaldal summary", answer_type="number", field="উপজেলা"
        )
        self.assertEqual(cert_upazila["status"], "supported")
        self.assertEqual(cert_upazila["value"], "500")

        # Verify Bengali digit representation is accepted by verify gate
        proposal_bengali = {
            "value": "৫০০",
            "evidence_ids": [e["id"] for e in cert_upazila["evidence"]],
        }
        result = self.gateway.verify(cert_upazila["certificate_id"], proposal_bengali)
        self.assertEqual(result["status"], "accepted")

    def test_pixel_charging_does_not_block_verify_or_text_resolve(self):
        snapshot = self.register("<article><h2>Summary</h2><p>Price: 100</p></article>")
        cert = self.resolve(snapshot, subject="Summary", answer_type="number", field="Price")
        self.assertEqual(cert["value"], "100")

        # Simulate exhausted pixel budget on this session
        with self.store.connect() as db:
            db.execute(
                "INSERT INTO sessions VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET image_pixels=30000000",
                (self.gateway.session_id, 2, 30_000_000),
            )

        # verify_answer has image_pixels=0 and must still succeed
        proposal = {
            "value": "100",
            "evidence_ids": [e["id"] for e in cert["evidence"]],
        }
        result = self.gateway.verify(cert["certificate_id"], proposal)
        self.assertEqual(result["status"], "accepted")


class MCPIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_three_tool_surface_and_real_calls(self):
        from fastmcp import Client

        from scripts.mcp_evidence_gateway import create_server

        with tempfile.TemporaryDirectory() as folder:
            gateway = Gateway(folder)
            registered = gateway.store.ingest(b"<p>Travel offer Code: MCPN10</p>")
            async with Client(create_server(gateway)) as client:
                tools = await client.list_tools()
                self.assertEqual(
                    {t.name for t in tools},
                    {"resolve_evidence", "inspect_evidence", "verify_answer"},
                )
                result = await client.call_tool(
                    "resolve_evidence",
                    {
                        "request": {
                            "source": {
                                "kind": "snapshot",
                                "id": registered["snapshot_id"],
                            },
                            "subject": "Travel offer",
                            "answer_type": "exact_code",
                        }
                    },
                )
                data = result.data
                cert = data["certificate"]
                self.assertEqual(cert["value"], "MCPN10")
                verified = await client.call_tool(
                    "verify_answer",
                    {
                        "certificate_id": cert["certificate_id"],
                        "proposed_answer": {
                            "value": "MCPN10",
                            "evidence_ids": [e["id"] for e in cert["evidence"]],
                        },
                    },
                )
                self.assertEqual(verified.data["status"], "accepted")
                viewed = await client.call_tool(
                    "inspect_evidence", {"evidence_id": cert["evidence"][0]["id"]}
                )
                self.assertTrue(viewed.content)
                from PIL import Image

                buffer = io.BytesIO()
                Image.new("RGB", (10, 10), "blue").save(buffer, format="PNG")
                saved = gateway.store.ingest(
                    b"<p>Image</p>", [{"bytes": buffer.getvalue()}]
                )
                index, _ = compile_capture(gateway.store, saved["capture_id"])
                region = next(
                    r for r in index["records"] if r["source_kind"] == "image_region"
                )
                cropped = await client.call_tool(
                    "inspect_evidence", {"evidence_id": region["id"], "view": "crop"}
                )
                self.assertTrue(any(block.type == "image" for block in cropped.content))

    async def test_standalone_stdio_server(self):
        import sys

        from fastmcp import Client

        with tempfile.TemporaryDirectory() as folder:
            store = Store(folder)
            saved = store.ingest(b"<p>Travel offer Code: STDIO10</p>")
            script = (
                Path(__file__).resolve().parents[1] / "scripts/mcp_evidence_gateway.py"
            )
            config = {
                "mcpServers": {
                    "v2": {
                        "command": sys.executable,
                        "args": [str(script)],
                        "env": {"LWA_V2_STORE": folder, "LWA_V2_ALLOW_LIVE": "0"},
                    }
                }
            }
            async with Client(config) as client:
                result = await client.call_tool(
                    "resolve_evidence",
                    {
                        "request": {
                            "source": {"kind": "snapshot", "id": saved["snapshot_id"]},
                            "subject": "Travel offer",
                            "answer_type": "exact_code",
                        }
                    },
                )
                self.assertEqual(result.data["certificate"]["value"], "STDIO10")


class ExtendedGatewayTests(GatewayFixture):
    def test_nested_fields_cannot_supply_another_subjects_name(self):
        snapshot = self.register(
            "<article>Travel offer<article>Local offer<dl><dt>Name</dt><dd>Alice</dd></dl></article></article>"
        )
        cert = self.resolve(snapshot, answer_type="exact_entity", field="Name")
        self.assertIsNone(cert["value"])

    def test_inspection_of_oversized_sequence_is_bounded(self):
        saved = self.store.ingest(
            ("<ol>" + "<li>" + "x" * 3000 + "</li></ol>").encode()
        )
        index, _ = compile_capture(self.store, saved["capture_id"])
        record = next(r for r in index["records"] if r["source_kind"] == "dom_sequence")
        result, _ = self.gateway.inspect(record["id"])
        self.assertTrue(result["truncated"])
        self.assertLessEqual(sum(map(len, result["items"])), 1600)

    def test_current_certificate_is_checked_again_at_emission(self):
        from datetime import datetime, timedelta

        now = datetime.now(UTC)
        snapshot = self.register(
            "<p>Travel offer Code: FRESH10</p>",
            mode="live_http",
            captured_at=now.isoformat(),
        )
        cert = self.resolve(snapshot, as_of="current")
        self.assertEqual(cert["status"], "supported")

        class Later(datetime):
            @classmethod
            def now(cls, tz=None):
                return now + timedelta(minutes=10)

        with patch("scripts.evidence_gateway.protocol.datetime", Later):
            result = self.gateway.verify(
                cert["certificate_id"],
                {
                    "value": "FRESH10",
                    "evidence_ids": [e["id"] for e in cert["evidence"]],
                },
            )
        self.assertEqual(result["reason"], "certificate_stale_at_verification")

    def test_temporal_reference_reports_both_observations(self):
        old = self.register(
            "<article>App statistics <p>Downloads: 400000+</p></article>",
            captured_at="2026-01-01T00:00:00Z",
            requested_url="https://example.org/app",
        )
        new = self.register(
            "<article>App statistics <p>Downloads: 500000+</p></article>",
            captured_at="2026-02-01T00:00:00Z",
            requested_url="https://example.org/app",
        )
        cert = self.resolve(
            new,
            subject="App statistics",
            answer_type="number",
            field="Downloads",
            compare_to=old,
        )
        self.assertEqual(cert["status"], "temporal_difference")
        self.assertEqual(
            [v["value"] for v in cert["comparison"]], ["500000+", "400000+"]
        )
        self.assertIsNone(cert["value"])

    def test_unknown_reference_alignment_does_not_establish_drift(self):
        old = self.register(
            "<article>App statistics <p>Downloads: 400000+</p></article>"
        )
        new = self.register(
            "<article>App statistics <p>Downloads: 500000+</p></article>"
        )
        cert = self.resolve(
            new,
            subject="App statistics",
            answer_type="number",
            field="Downloads",
            compare_to=old,
        )
        self.assertEqual(cert["status"], "unresolved_reference")

    def test_nested_cards_never_borrow_inner_coupon(self):
        for html in (
            "<article>Travel offer 7%<article>Local offer 9% Code: WRONG10</article></article>",
            "<article><h2>Travel offer 7%</h2><article><h2>Local offer 9%</h2>Code: WRONG10</article></article>",
        ):
            cert = self.resolve(self.register(html), qualifiers={"discount": "7%"})
            self.assertIsNone(cert["value"])

    def test_heading_binds_a_nested_field_without_card_classes(self):
        snapshot = self.register(
            "<div><h2>Travel offer</h2><div><span>Code: NESTED10</span></div></div>"
        )
        self.assertEqual(self.resolve(snapshot)["value"], "NESTED10")

    def test_timeout_terminates_a_slow_adapter(self):
        import sys

        from PIL import Image

        buffer = io.BytesIO()
        Image.new("RGB", (10, 10)).save(buffer, format="PNG")
        snapshot = self.store.ingest(
            b"<p>Travel offer</p>", [{"bytes": buffer.getvalue()}]
        )["snapshot_id"]
        marker = self.root / "should-not-exist"
        adapter = self.root / "slow.py"
        adapter.write_text(
            "import time\nfrom pathlib import Path\ntime.sleep(3)\nPath("
            + repr(str(marker))
            + ").write_text('finished')\n"
        )
        with patch.dict(
            os.environ,
            {
                "LWA_V2_VISION_ID": "slow-test",
                "LWA_V2_VISION_COMMAND": json.dumps([sys.executable, str(adapter)]),
            },
        ):
            start = time.monotonic()
            cert = self.resolve(
                snapshot,
                budget={"max_wall_ms": 500, "max_ocr_calls": 0, "max_vision_calls": 1},
            )
            self.assertLess(time.monotonic() - start, 1.5)
        self.assertEqual(cert["status"], "coverage_incomplete")
        self.assertFalse(marker.exists())

    def test_configured_vision_adapter_is_bounded_and_cached(self):
        import sys

        from PIL import Image

        buffer = io.BytesIO()
        Image.new("RGB", (10, 10)).save(buffer, format="PNG")
        snapshot = self.store.ingest(
            b"<p>Travel offer</p>", [{"bytes": buffer.getvalue()}]
        )["snapshot_id"]
        adapter = self.root / "vision.py"
        adapter.write_text(
            'import sys,json\nx=json.load(sys.stdin)\nassert x["image_png_base64"]\nprint(json.dumps({"model_id":x["model_id"],"text":"Travel offer Code: READ10","usage":{"input_tokens":12,"output_tokens":7}}))\n'
        )
        with patch.dict(
            os.environ,
            {
                "LWA_V2_VISION_ID": "fixture-reader-v1",
                "LWA_V2_VISION_COMMAND": json.dumps([sys.executable, str(adapter)]),
            },
        ):
            request = self.request(
                snapshot, budget={"max_ocr_calls": 0, "max_vision_calls": 1}
            )
            first = self.gateway.resolve(request)
            self.assertEqual(first["usage"]["vision_calls"], 1)
            self.assertEqual(
                first["certificate"]["status"], "ambiguous"
            )  # one reading is not corroboration
            request["question"] = "Repeat the exact code"
            second = self.gateway.resolve(request)
            self.assertEqual(second["usage"]["vision_calls"], 0)
            self.assertEqual(second["usage"]["vision_cache_hits"], 1)
            self.assertEqual(second["certificate"]["candidates"], ["READ10"])


class RuntimeIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("LWA_V2_TEST_OCR") == "1",
        "enable LWA_V2_TEST_OCR with a configured Tesseract runtime",
    )
    def test_real_ocr_reads_saved_pixels_and_caches(self):
        from PIL import Image, ImageDraw, ImageFont

        with tempfile.TemporaryDirectory() as folder:
            image = Image.new("RGB", (1000, 130), "white")
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 36)
            ImageDraw.Draw(image).text(
                (20, 40), "Travel offer Code: READN10", fill="black", font=font
            )
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            gateway = Gateway(folder)
            registered = gateway.store.ingest(
                b"<p>Image-only promotion</p>", [{"bytes": buffer.getvalue()}]
            )
            request = {
                "source": {"kind": "snapshot", "id": registered["snapshot_id"]},
                "subject": "Travel offer",
                "answer_type": "exact_code",
                "budget": {"max_visual_regions": 1, "max_ocr_calls": 2},
            }
            result = gateway.resolve(request)
            cert = result["certificate"]
            if cert["status"] == "corroborated_visual":
                self.assertEqual(cert["value"], "READN10")
            else:
                self.assertEqual(cert["status"], "ambiguous")
                self.assertIsNone(cert["value"])
                self.assertIn("READN10", cert["candidates"])
            self.assertEqual(result["usage"]["ocr_calls"], 2)
            request["question"] = "What is the exact code?"
            second = gateway.resolve(request)
            self.assertEqual(second["usage"]["ocr_calls"], 0)
            self.assertEqual(second["usage"]["ocr_cache_hits"], 2)

    @unittest.skipUnless(
        os.environ.get("LWA_V2_TEST_BROWSER") == "1",
        "enable LWA_V2_TEST_BROWSER with installed Chromium",
    )
    def test_local_browser_hydration_geometry_and_hidden_css(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        from threading import Thread

        class Page(BaseHTTPRequestHandler):
            def do_GET(self):
                data = b"""<html><head><style>.hidden {display:none}</style></head><body>
                <article class="hidden">Travel offer Code: WRONG10</article>
                <article id="offer"></article><script>document.getElementById('offer').textContent='Travel offer Code: BROWSERN10';</script>
                </body></html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *_):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Page)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with (
                tempfile.TemporaryDirectory() as folder,
                patch.dict(os.environ, {"LWA_V2_ALLOW_LIVE": "1"}),
            ):
                gateway = Gateway(folder)
                result = gateway.resolve(
                    {
                        "source": {
                            "kind": "live",
                            "url": f"http://127.0.0.1:{server.server_port}",
                            "render": "browser",
                        },
                        "subject": "Travel offer",
                        "answer_type": "exact_code",
                    }
                )
                self.assertEqual(result["certificate"]["value"], "BROWSERN10")
                manifest = gateway.store.get(result["certificate"]["capture_id"])
                self.assertTrue(manifest["geometry"])
                self.assertEqual(manifest["images"][0]["role"], "rendered_screenshot")
                automatic = gateway.resolve(
                    {
                        "source": {
                            "kind": "live",
                            "url": f"http://127.0.0.1:{server.server_port}",
                            "render": "auto",
                        },
                        "subject": "Travel offer",
                        "answer_type": "exact_code",
                    }
                )
                self.assertEqual(automatic["certificate"]["value"], "BROWSERN10")
                self.assertTrue(automatic["usage"]["browser_escalated"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
