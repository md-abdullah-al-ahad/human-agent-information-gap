"""Immutable source blobs and records, mutable lookup caches, and session counters."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sqlite3
import tempfile
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

MAX_HTML_BYTES = 4_000_000
MAX_IMAGE_BYTES = 8_000_000
MAX_IMAGES = 12
MAX_SOURCE_PIXELS = 80_000_000
HANDLE = re.compile(r"^([a-z]+):([0-9a-f]{64})$")


def encode(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def utcnow():
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def timestamp(value):
    if value is None:
        return None
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("capture time must include a timezone")
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def split_handle(handle, kind=None):
    match = HANDLE.fullmatch(str(handle))
    if not match or (kind is not None and match[1] != kind):
        raise ValueError(f"invalid {kind or 'evidence'} handle")
    return match[1], match[2]


class Store:
    def __init__(self, root=None):
        self.root = (
            Path(
                root
                or os.environ.get("LWA_V2_STORE", Path.home() / ".cache/lwa-web/v2")
            )
            .expanduser()
            .resolve()
        )
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with self.connect() as db:
            db.executescript("""
              PRAGMA journal_mode=WAL;
              CREATE TABLE IF NOT EXISTS records (kind TEXT, id TEXT, data BLOB, PRIMARY KEY(kind,id));
              CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, data BLOB);
              CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, calls INTEGER, image_pixels INTEGER);
              CREATE TABLE IF NOT EXISTS audit (at TEXT, session TEXT, operation TEXT, data BLOB);
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.root / "store.sqlite3", timeout=10)
        try:
            with db:
                yield db
        finally:
            db.close()

    def blob(self, data):
        sha = digest(data)
        path = self.root / "blobs" / sha[:2] / sha
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
                f.write(data)
                temporary = f.name
            try:
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return sha

    def read_blob(self, sha):
        if not re.fullmatch(r"[0-9a-f]{64}", str(sha)):
            raise ValueError("invalid blob hash")
        data = (self.root / "blobs" / sha[:2] / sha).read_bytes()
        if digest(data) != sha:
            raise ValueError("source blob integrity check failed")
        return data

    def put(self, kind, value):
        raw = encode(value)
        key = digest(raw)
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO records VALUES (?,?,?)", (kind, key, raw))
        return f"{kind}:{key}"

    def put_many(self, kind, values):
        rows = [(kind, digest(encode(v)), encode(v)) for v in values]
        with self.connect() as db:
            db.executemany("INSERT OR IGNORE INTO records VALUES (?,?,?)", rows)
        return [f"{kind}:{row[1]}" for row in rows]

    def get(self, handle, expected_kind=None):
        kind, key = split_handle(handle, expected_kind)
        with self.connect() as db:
            row = db.execute(
                "SELECT data FROM records WHERE kind=? AND id=?", (kind, key)
            ).fetchone()
        if row is None:
            raise ValueError(f"unknown {kind} handle")
        if digest(row[0]) != key:
            raise ValueError("record integrity check failed")
        return json.loads(row[0])

    def cached(self, key):
        with self.connect() as db:
            row = db.execute("SELECT data FROM cache WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def cache(self, key, value):
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO cache VALUES (?,?)", (key, encode(value)))
        return self.cached(key)

    def charge(self, session, max_calls, image_pixels=0, max_image_pixels=8_000_000):
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO sessions VALUES (?,0,0)", (session,))
            result = db.execute(
                """UPDATE sessions SET calls=calls+1, image_pixels=image_pixels+?
                WHERE id=? AND calls<? AND image_pixels+?<=?""",
                (image_pixels, session, max_calls, image_pixels, max_image_pixels),
            )
            if not result.rowcount:
                raise ValueError("session call or image-pixel budget exhausted")

    def audit(self, session, operation, data):
        with self.connect() as db:
            db.execute(
                "INSERT INTO audit VALUES (?,?,?,?)",
                (utcnow(), session, operation, encode(data)),
            )

    def ingest(
        self,
        html,
        images=(),
        *,
        mode="snapshot",
        requested_url=None,
        final_url=None,
        captured_at=None,
        http_status=None,
        geometry=None,
        network=(),
        coverage=None,
    ):
        if len(html) > MAX_HTML_BYTES or len(images) > MAX_IMAGES:
            raise ValueError("capture exceeds HTML or image-count limit")
        stored_images = []
        for image in images:
            data = image["bytes"]
            if len(data) > MAX_IMAGE_BYTES:
                raise ValueError("image exceeds byte limit")
            import io

            from PIL import Image

            with Image.open(io.BytesIO(data)) as opened:
                width, height = opened.size
                if width * height > MAX_SOURCE_PIXELS:
                    raise ValueError("image exceeds pixel limit")
                opened.verify()
            stored_images.append(
                {
                    "sha256": self.blob(data),
                    "width": width,
                    "height": height,
                    "role": image.get("role", "asset"),
                    "locator": image.get("locator"),
                    "url": image.get("url"),
                }
            )
        stored_network = []
        if len(network) > 8:
            raise ValueError("at most eight network records")
        for response in network:
            raw = encode(response["json"])
            if len(raw) > 500_000:
                raise ValueError("network JSON exceeds byte limit")
            stored_network.append(
                {
                    "sha256": self.blob(raw),
                    "url": response.get("url"),
                    "captured_at": timestamp(response.get("captured_at")),
                }
            )
        # Observation times belong to the acquisition, not the reusable source identity.
        manifest = {
            "html_sha256": self.blob(html),
            "images": stored_images,
            "geometry": geometry or [],
            "network": [
                {k: v for k, v in r.items() if k != "captured_at"}
                for r in stored_network
            ],
        }
        capture_id = self.put("capture", manifest)
        event = {
            "capture_id": capture_id,
            "mode": mode,
            "requested_url": requested_url,
            "final_url": final_url,
            "http_status": http_status,
            "captured_at": timestamp(captured_at),
            "registered_at": utcnow(),
            "nonce": secrets.token_hex(8),
            "network_times": [r["captured_at"] for r in stored_network],
            "coverage": coverage or ["saved_html", "interactive_states_unchecked"],
        }
        snapshot_id = self.put("snapshot", event)
        return {
            "snapshot_id": snapshot_id,
            "capture_id": capture_id,
            "captured_at": event["captured_at"],
            "images": len(stored_images),
        }

    def register(
        self, allowed_root, html_path, image_paths=(), *, captured_at=None, url=None
    ):
        """Administrative operation; never exposed as an agent tool."""
        root = Path(allowed_root).resolve(strict=True)

        def read(path, maximum):
            path = Path(path)
            resolved = (path if path.is_absolute() else root / path).resolve(
                strict=True
            )
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError("snapshot file is outside the registration root")
            with resolved.open("rb") as f:
                data = f.read(maximum + 1)
            if len(data) > maximum:
                raise ValueError("snapshot file exceeds byte limit")
            return data

        if len(image_paths) > MAX_IMAGES:
            raise ValueError("too many snapshot images")
        return self.ingest(
            read(html_path, MAX_HTML_BYTES),
            [
                {"bytes": read(p, MAX_IMAGE_BYTES), "role": "saved_image"}
                for p in image_paths
            ],
            captured_at=captured_at,
            requested_url=url,
        )
