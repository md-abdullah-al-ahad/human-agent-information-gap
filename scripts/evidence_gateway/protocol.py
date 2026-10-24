"""Strict requests and conservative answer extraction; no generated summaries."""

from __future__ import annotations

import re
from datetime import UTC, datetime

from .compiler import norm, terms
from .store import split_handle, timestamp

ANSWER_TYPES = {
    "exact_code",
    "exact_entity",
    "number",
    "date",
    "set",
    "instruction",
    "status",
    "quote",
}
ALLOWED = {
    "source",
    "question",
    "answer_type",
    "subject",
    "qualifiers",
    "field",
    "scope",
    "as_of",
    "position",
    "budget",
    "evidence_ids",
    "compare_to",
}
DEFAULT_BUDGET = {
    "max_wall_ms": 20000,
    "max_visual_regions": 3,
    "max_ocr_calls": 4,
    "max_vision_calls": 0,
}
MAX_BUDGET = {
    "max_wall_ms": 60000,
    "max_visual_regions": 6,
    "max_ocr_calls": 8,
    "max_vision_calls": 1,
}
DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def bounded_string(value, label, maximum, required=False):
    if (
        not isinstance(value, str)
        or len(value) > maximum
        or (required and not value.strip())
    ):
        raise ValueError(
            f"{label} must be {'nonempty ' if required else ''}text of at most {maximum} characters"
        )
    return norm(value)


def validate_request(request):
    if not isinstance(request, dict) or set(request) - ALLOWED:
        raise ValueError("unknown request fields")
    source = request.get("source")
    if not isinstance(source, dict):
        raise ValueError("source is required")  # noqa: TRY004 -- consistent public validation errors
    kind = source.get("kind")
    if kind == "snapshot":
        if set(source) != {"kind", "id"}:
            raise ValueError("snapshot source requires only kind and registered id")
        split_handle(source["id"], "snapshot")
    elif kind == "live":
        if set(source) - {"kind", "url", "render"}:
            raise ValueError("unknown live source fields")
        from urllib.parse import urlparse

        parsed = urlparse(bounded_string(source.get("url"), "URL", 2048, True))
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            raise ValueError("live source requires an HTTP(S) URL without credentials")
        if source.get("render", "auto") not in {"http", "browser", "auto"}:
            raise ValueError("render must be http, browser, or auto")
    else:
        raise ValueError("source.kind must be snapshot or live")
    answer_type = request.get("answer_type")
    if answer_type not in ANSWER_TYPES:
        raise ValueError("unsupported answer_type")
    result = {
        "source": dict(source),
        "question": bounded_string(request.get("question", ""), "question", 500),
        "answer_type": answer_type,
        "subject": bounded_string(request.get("subject", ""), "subject", 160, True),
        "field": bounded_string(request.get("field", ""), "field", 80),
        "scope": request.get("scope", "page"),
        "as_of": request.get("as_of", "capture"),
        "position": request.get("position"),
        "qualifiers": {},
        "budget": dict(DEFAULT_BUDGET),
        "evidence_ids": [],
    }
    result["compare_to"] = request.get("compare_to")
    if result["compare_to"] is not None:
        split_handle(result["compare_to"], "snapshot")
    if result["scope"] not in {"page", "data", "all_sources"}:
        raise ValueError("scope must be page, data, or all_sources")
    if result["as_of"] not in {"capture", "current"}:
        result["as_of"] = timestamp(result["as_of"])
    position = result["position"]
    if position is not None and (
        type(position) is not int or not 1 <= position <= 1000
    ):
        raise ValueError("position must be an integer between 1 and 1000")
    qualifiers = request.get("qualifiers", {})
    if not isinstance(qualifiers, dict) or len(qualifiers) > 6:
        raise ValueError("at most six qualifiers")
    result["qualifiers"] = {
        bounded_string(k, "qualifier key", 40, True): bounded_string(
            v, "qualifier", 80, True
        )
        for k, v in sorted(qualifiers.items())
    }
    budget = request.get("budget", {})
    if not isinstance(budget, dict) or set(budget) - set(MAX_BUDGET):
        raise ValueError("unknown budget field")
    for name, value in budget.items():
        minimum = 100 if name == "max_wall_ms" else 0
        if type(value) is not int or not minimum <= value <= MAX_BUDGET[name]:
            raise ValueError(f"{name} must be between {minimum} and {MAX_BUDGET[name]}")
        result["budget"][name] = value
    ids = request.get("evidence_ids", [])
    if not isinstance(ids, list) or len(ids) > 3:
        raise ValueError("at most three evidence IDs")
    for handle in ids:
        split_handle(handle, "ev")
    result["evidence_ids"] = sorted(set(ids))
    return result


def searchable(record):
    return norm(
        " ".join(str(record.get(k, "")) for k in ("text", "context", "anchor", "field"))
    )


def phrase_present(phrase, text):
    phrase = norm(phrase).casefold().translate(DIGITS)
    text = norm(text).casefold().translate(DIGITS)
    return bool(
        re.search(
            r"(?<![\w\u0980-\u09ff])" + re.escape(phrase) + r"(?![\w\u0980-\u09ff])",
            text,
        )
    )


def bound_to_question(record, query):
    text = searchable(record)
    # Subject is an entity or container label, not a whole natural-language question.
    if not phrase_present(query["subject"], text):
        return False
    if not all(phrase_present(value, text) for value in query["qualifiers"].values()):
        return False
    if record.get("truncated"):
        return False
    if (
        query["position"] is not None
        and (record.get("sequence") or {}).get("position") != query["position"]
    ):
        return False
    # Arbitrary OCR blocks can span cards. Do not bind a requested percentage
    # when the same block contains a competing percentage.
    percentages = set(re.findall(r"\d+(?:\.\d+)?\s*%", text.translate(DIGITS)))
    return not (record["source_kind"] == "visual_reading" and len(percentages) > 1)


def ranked_records(records, query):
    requested = terms(
        query["question"]
        + " "
        + query["subject"]
        + " "
        + query["field"]
        + " "
        + " ".join(query["qualifiers"].values())
    )
    ranked = []
    for record in records:
        is_data = record["source_kind"] in {"embedded_json", "network_json"}
        if query["scope"] == "page" and is_data:
            continue
        if query["scope"] == "data" and not is_data:
            continue
        overlap = len(requested & terms(searchable(record)))
        if overlap or record["id"] in query["evidence_ids"]:
            rank = 100 * int(bound_to_question(record, query)) + overlap
            ranked.append((-rank, record.get("order", 0), record["id"], record))
    return [r[-1] for r in sorted(ranked)]


def extract_values(record, query):
    """Only extract within the bound source unit; no inferred real-world claims."""
    text, field = record["text"], query["field"]
    source = record["source_kind"]
    data = source in {"embedded_json", "network_json"}
    selected = None
    if field:
        if data:
            if record.get("field", "").casefold() != field.casefold():
                return []
            selected = text
        else:
            if (
                len(
                    re.findall(
                        r"(?<!\w)" + re.escape(field) + r"\s*[:：]", text, re.IGNORECASE
                    )
                )
                > 1
            ):
                return []
            values = [
                value
                for label, value in record.get("fields", [])
                if label.casefold() == field.casefold()
            ]
            if len(set(values)) == 1:
                selected = values[0]
            elif len(set(values)) > 1:
                return []
            else:
                match = re.search(
                    r"(?<!\w)" + re.escape(field) + r"\s*[:：]\s*([^;\n|]+)",
                    text,
                    re.IGNORECASE,
                )
                if match:
                    selected = match[1].strip()
                else:
                    m_after = re.search(
                        r"(?<!\w)" + re.escape(field) + r"\s+([0-9০-৯]+[\d,০-৯]*(?:\.[0-9০-৯]+)?(?:\s*(?:million|billion|thousand|crore|lakh|কোটি|লাখ))?)",
                        text,
                        re.IGNORECASE,
                    )
                    if m_after:
                        selected = m_after[1].strip()
                    else:
                        m_before = re.search(
                            r"([0-9০-৯]+[\d,০-৯]*(?:\.[0-9০-৯]+)?(?:\s*(?:million|billion|thousand|crore|lakh|কোটি|লাখ))?)\s+" + re.escape(field),
                            text,
                            re.IGNORECASE,
                        )
                        if m_before:
                            selected = m_before[1].strip()
            if selected is None:
                return []
    kind = query["answer_type"]
    if kind in {"instruction", "set"} and record.get("tag") in {
        "h1",
        "h2",
        "h3",
        "h4",
        "dt",
    }:
        return []
    value_text = selected if selected is not None else text
    if kind == "exact_code":
        labeled = re.findall(
            r"(?:coupon|promo|voucher)?\s*code\s*[:：]\s*([A-Za-z0-9_-]{3,32})(?![A-Za-z0-9_-])",
            value_text,
            re.IGNORECASE,
        )
        values = labeled or re.findall(
            r"(?<![A-Za-z0-9_-])(?=[A-Z0-9_-]{4,32}(?![A-Za-z0-9_-]))(?=[A-Z0-9_-]*[A-Z])(?=[A-Z0-9_-]*[0-9])[A-Z0-9_-]{4,32}(?![A-Za-z0-9_-])",
            value_text,
        )
        return sorted(set(values))
    if kind == "exact_entity":
        # A typed field prevents silently using a neighboring child's/parent's name.
        if selected is None:
            for label in ("name", "নাম"):
                if (
                    len(
                        re.findall(
                            r"(?<!\w)" + label + r"\s*[:：]", text, re.IGNORECASE
                        )
                    )
                    > 1
                ):
                    return []
                match = re.search(
                    r"(?<!\w)" + label + r"\s*[:：]\s*([^;|\n]+)", text, re.IGNORECASE
                )
                if match:
                    return [match[1].strip()]
            return []
        return [selected] if selected else []
    if kind == "number":
        if selected is None and not data:
            return []  # Multiple unlabeled numbers on a card are not a typed answer.
        matches = re.findall(
            r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?(?:[eE][+-]?\d+)?(?:\s*%|\+)?(?!\w)",
            value_text.translate(DIGITS),
        )
        return sorted({m.replace(",", "").replace(" ", "") for m in matches})
    if kind == "date":
        # Keep unambiguous ISO dates; ambiguous 03/04/2026 is unresolved.
        values = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", value_text.translate(DIGITS))
        return sorted({v for v in values if valid_date(v)})
    if kind == "status":
        if "?" in value_text or re.search(
            r"\b(may|might|could|if|possibly|unknown|but|however)\b",
            value_text,
            re.IGNORECASE,
        ):
            return []
        if selected is None:
            statement = re.search(
                re.escape(query["subject"]) + r"\s+(?:is|are)\s+([^.;!?]+)",
                text,
                re.IGNORECASE,
            )
            if not statement:
                return []
            value_text = statement[1]
        patterns = {
            "out_of_stock": r"^(?:currently )?(?:out of stock|unavailable)\b",
            "in_stock": r"^(?:currently )?in stock\b",
            "incompatible": r"^(?:not compatible|incompatible)\b",
            "compatible": r"^compatible with\b",
        }
        return [
            name
            for name, pattern in patterns.items()
            if re.search(pattern, value_text, re.IGNORECASE)
        ]
    if kind in {"instruction", "quote", "set"}:
        return [value_text] if value_text else []
    return []


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def stale_reason(query, event):
    if query["as_of"] == "capture":
        return None
    captured = event.get("captured_at")
    if not captured:
        return "The capture time is unknown; it cannot support the requested time."
    when = datetime.fromisoformat(captured)
    if query["as_of"] == "current":
        if (
            event["mode"] == "snapshot"
            or abs((datetime.now(UTC) - when).total_seconds()) > 300
        ):
            return "This saved observation does not establish the current page state."
    elif captured != query["as_of"]:
        return "The capture and requested observation times differ."
    return None
