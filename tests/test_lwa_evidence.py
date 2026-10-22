"""Contract checks on saved captures; these are not new agent experiments."""

import unittest
import os
import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from scripts.lwa_evidence import PageTextParser, inspect_page, _acquire_live_images, _network_json_matches, _ocr_file
from scripts.lwa_evidence_store import (inspect_evidence, inspect_image_crop,
                                        check_claim, check_structured_claim, save_capture)
from scripts.build_adjudication_worklist import build_rows
from scripts.prepare_offline_agent_pilot import build_packet, verify_manifest


ROOT = Path(__file__).resolve().parents[1]


class EvidenceContractTests(unittest.TestCase):
    def setUp(self):
        store = tempfile.TemporaryDirectory()
        self.addCleanup(store.cleanup)
        environment = patch.dict(os.environ, {"LWA_EVIDENCE_DIR": store.name})
        environment.start()
        self.addCleanup(environment.stop)

    def test_cloudflare_capture_is_blocked(self):
        result = inspect_page(str(ROOT / "data/stage-4/raw/bd-tr02-dom.html"),
                              "Which flights are available?", mode="snapshot")
        self.assertEqual(result["capture"]["access"], "blocked")
        self.assertEqual(result["observations"], [])
        self.assertEqual(result["unresolved"][0]["state"], "access_blocked")

    def test_purchase_question_does_not_infer_stock(self):
        result = inspect_page(str(ROOT / "data/stage-4/raw/bd-qc02-dom.html"),
                              "Is Egg Loose in stock?", mode="snapshot")
        self.assertEqual(result["capture"]["access"], "ok")
        self.assertIsNone(result["capture"]["captured_at_utc"])
        self.assertIn("unknown", {entry["state"] for entry in result["unresolved"]})
        self.assertIn("image_unchecked", {entry["state"] for entry in result["unresolved"]})
        self.assertTrue(all(entry["state"] != "ocr_candidate" for entry in result["observations"]))

    def test_snapshot_time_and_missing_ocr_are_explicit(self):
        with patch("scripts.lwa_evidence.shutil.which", return_value=None):
            result = inspect_page(str(ROOT / "data/stage-4/raw/bd-qc02-dom.html"),
                                  "What is the Puja coupon code?", mode="snapshot",
                                  snapshot_captured_at_utc="2026-10-18T22:40:11Z",
                                  image_paths=[str(ROOT / "data/stage-4/screenshots/bd-qc02-fullpage.png")])
        self.assertEqual(result["capture"]["captured_at_source"], "caller_supplied")
        self.assertEqual(result["capture"]["captured_at_utc"], "2026-10-18T22:40:11Z")
        self.assertIn("historical_snapshot", {item["state"] for item in result["unresolved"]})
        self.assertIn("ocr_unavailable_or_failed", {item["state"] for item in result["unresolved"]})
        self.assertFalse(any(item.get("text") == "PUJA6" for item in result["observations"]))

    def test_embedded_chaldal_state_is_not_called_visible_page_text(self):
        result = inspect_page(str(ROOT / "data/stage-4/raw/chaldal-dom.html"),
                              "What is the marketing banner StartTime?", mode="snapshot")
        state = [item for item in result["observations"]
                 if item["source"] == "window.__serviceState"]
        self.assertTrue(state)
        self.assertEqual(state[0]["human_visibility"], "unverified")
        self.assertIn("StartTime", state[0]["locator"])

    def test_explicit_snapshot_mode_rejects_a_url(self):
        with self.assertRaises(ValueError):
            inspect_page("https://example.com", mode="snapshot")

    def test_saved_handle_resolves_quote_but_abstains_on_stock_inference(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"LWA_EVIDENCE_DIR": folder}):
            page = Path(folder) / "sample.html"
            page.write_text("<html><body><p>Blue model</p><button>Buy Now</button></body></html>")
            result = inspect_page(str(page), "Blue model", mode="snapshot")
            handle = result["capture"]["id"]
            observation = next(item for item in result["observations"] if item["text"] == "Blue model")
            inspected = inspect_evidence(handle, [observation["id"]])
            self.assertEqual(inspected["observations"][0]["text"], "Blue model")
            self.assertIn("Blue model", inspected["observations"][0]["source_excerpt"])
            self.assertEqual(check_claim(handle, "Blue model", [observation["id"]])["status"], "supported")
            self.assertEqual(check_claim(handle, "Blue model is in stock", [observation["id"]])["status"],
                             "insufficient_evidence")
            with self.assertRaises(ValueError):
                inspect_evidence("../bad-handle", [observation["id"]])

    def test_network_json_keeps_separate_provenance(self):
        matches = _network_json_matches([{"url": "https://example.org/api", "sha256": "abc",
                                          "captured_at_utc": "2026-10-21T00:00:00Z",
                                          "json": {"product": {"price": 42}}}], {"price"})
        self.assertEqual(matches[0]["source"], "network_json")
        self.assertEqual(matches[0]["locator"], "$.product.price")
        self.assertEqual(matches[0]["response_url"], "https://example.org/api")

    def test_ocr_candidate_is_not_claim_support(self):
        handle = save_capture({"requested": "sample", "acquired_at_utc": "2026-10-21T00:00:00Z",
                               "content_sha256": hashlib.sha256(b"<html></html>").hexdigest(),
                               "mode": "snapshot"}, b"<html></html>",
                              [{"id": "obs-001", "source": "ocr_tesseract", "state": "ocr_candidate",
                                "text": "PUJA6", "exactness": "unverified"}])
        self.assertEqual(check_claim(handle, "PUJA6", ["obs-001"])["status"], "insufficient_evidence")

    def test_structured_claim_requires_explicit_subject_bound_statement(self):
        observations = [
            {"id": "obs-001", "source": "html_text_node", "state": "observed_text",
             "text": "Blue model is out of stock"},
            {"id": "obs-002", "source": "html_text_node", "state": "observed_text",
             "text": "Red model is in stock"},
            {"id": "obs-003", "source": "html_text_node", "state": "observed_text",
             "text": "Blue model Buy Now"},
            {"id": "obs-004", "source": "ocr_tesseract", "state": "ocr_candidate",
             "text": "Blue model is in stock"},
            {"id": "obs-005", "source": "html_text_node", "state": "observed_text",
             "text": "Blue model is not compatible with Case X"},
        ]
        handle = save_capture({"requested": "sample", "acquired_at_utc": "2026-10-21T00:00:00Z",
                               "content_sha256": hashlib.sha256(b"<html></html>").hexdigest(),
                               "mode": "snapshot"}, b"<html></html>", observations)
        def check(predicate, value, ids, object_name=""):
            return check_structured_claim(handle, "Blue model", predicate, value, ids, object_name)
        self.assertEqual(check("stock_status", "in_stock", ["obs-001"])["status"], "contradicted")
        self.assertEqual(check("stock_status", "out_of_stock", ["obs-001"])["status"], "supported")
        self.assertEqual(check("stock_status", "in_stock", ["obs-002", "obs-003", "obs-004"])["status"],
                         "insufficient_evidence")
        self.assertEqual(check("compatibility", "compatible", ["obs-005"], "Case X")["status"],
                         "contradicted")
        self.assertEqual(check("compatibility", "incompatible", ["obs-005"], "Case Y")["status"],
                         "insufficient_evidence")

    def test_image_crop_is_bound_to_saved_hash_and_original_coordinates(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is an optional image-crop dependency")
        from io import BytesIO
        image = Image.new("RGB", (4, 3), "red")
        image.putpixel((2, 1), (0, 0, 255))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        data = buffer.getvalue()
        digest = hashlib.sha256(data).hexdigest()
        handle = save_capture({"requested": "sample", "acquired_at_utc": "2026-10-21T00:00:00Z",
                               "content_sha256": hashlib.sha256(b"<html></html>").hexdigest(),
                               "mode": "snapshot"}, b"<html></html>", [], images=[{
                                   "bytes": data, "source_path": "saved-example.png"}])
        metadata, pixels = inspect_image_crop(handle, digest, [2, 1, 3, 2])
        self.assertEqual(metadata["bbox_original_pixels"], [2, 1, 3, 2])
        self.assertEqual(metadata["returned_dimensions"], [1, 1])
        self.assertEqual(Image.open(BytesIO(pixels)).getpixel((0, 0)), (0, 0, 255))
        with self.assertRaises(ValueError):
            inspect_image_crop(handle, "0" * 64, [2, 1, 3, 2])
        with self.assertRaises(ValueError):
            inspect_image_crop(handle, digest, [0, 0, 5, 1])

    def test_ocr_does_not_fill_question_with_unrelated_first_lines(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / "sample.png"
            image.write_bytes(b"sample-raster-bytes")
            output = ("level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
                      "5\t1\t1\t1\t1\t1\t0\t0\t40\t12\t95\tHome\n")
            from subprocess import CompletedProcess
            with patch("scripts.lwa_evidence.shutil.which", return_value="/usr/bin/tesseract"), \
                 patch("scripts.lwa_evidence.subprocess.run",
                       return_value=CompletedProcess([], 0, stdout=output, stderr="")):
                observations, error = _ocr_file(image, {"puja6"})
        self.assertEqual(observations, [])
        self.assertIn("no question-term match", error)

    def test_live_image_acquisition_uses_pixels_then_records_source(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self, *_):
                return b"sample-raster-bytes"

            def geturl(self):
                return "https://example.org/banner.png"

            @property
            def headers(self):
                from email.message import Message
                value = Message()
                value["content-type"] = "image/png"
                return value

        images = [{"src": "/banner.png", "alt": "Puja offer", "title": "",
                   "locator": "html:1:12"}]
        with patch("scripts.lwa_evidence.shutil.which", return_value="/usr/bin/tesseract"), \
             patch("scripts.lwa_evidence.urllib.request.urlopen", return_value=FakeResponse()), \
             patch("scripts.lwa_evidence._ocr_file", return_value=([{"source": "ocr_tesseract",
                                                                         "text": "PUJA6"}], None)):
            observations, artifacts, errors = _acquire_live_images(images, "https://example.org", {"puja"})
        self.assertEqual(errors, [])
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(observations[0]["text"], "PUJA6")
        self.assertEqual(observations[0]["locator"], "html:1:12")
        self.assertEqual(observations[0]["image_url"], "https://example.org/banner.png")
        self.assertEqual(observations[0]["image_sha256"], hashlib.sha256(b"sample-raster-bytes").hexdigest())

    def test_inline_css_background_is_an_image_candidate(self):
        parser = PageTextParser()
        parser.feed('<div style="background-image: url(https://example.org/offer.jpg)">Offer</div>')
        self.assertEqual(parser.images[0]["kind"], "css_background")
        self.assertEqual(parser.images[0]["src"], "https://example.org/offer.jpg")

    def test_adjudication_worklist_preserves_all_rows_without_new_accuracy(self):
        rows = build_rows()
        self.assertEqual(len(rows), 1010)
        self.assertEqual(len({row["item_id"] for row in rows}), 323)
        self.assertEqual(next(row for row in rows if row["item_id"] == "BD-TR03-04" and
                              "With Playwright" in row["agent_setup"])["corrected_outcome"],
                         "fail_exact_text")
        self.assertTrue(any(row["review_state"] == "pending" and not row["corrected_outcome"]
                            for row in rows))
        self.assertEqual(sum(row["review_state"] == "source_verified" for row in rows), 7)
        self.assertEqual(sum(row["review_state"] == "source_checked_unresolved" for row in rows), 4)
        self.assertEqual(next(row for row in rows if row["source_csv_row"] == "361")["corrected_outcome"],
                         "partial_brand_list")

    def test_frozen_pilot_packet_withholds_reference_answers(self):
        manifest = verify_manifest()
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "packet"
            build_packet(destination, manifest)
            index = json.loads((destination / "tasks.json").read_text(encoding="utf-8"))
            self.assertEqual(len(index["tasks"]), 22)
            self.assertEqual(sum(not task["diagnostic"] for task in index["tasks"]), 20)
            self.assertTrue(all("expected" not in task and "reference" not in task
                                for task in index["tasks"]))
            self.assertTrue(all("expected" not in site and "reference" not in site
                                for site in index["sites"].values()))
            self.assertNotIn("USBA15", json.dumps(index))
            self.assertNotIn("PUJA6", json.dumps(index))
            self.assertTrue((destination / index["sites"]["usbair"]["dom_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
