"""Reproducible local demonstration; no website, agent, or paid model is called."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evidence_gateway.gateway import Gateway
from evidence_gateway.store import encode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store")
    parser.add_argument("--output")
    args = parser.parse_args()
    gateway = Gateway(args.store)
    page = (
        "<html><body><section><article><h2>Travel offer 7%</h2><p>Code: DEMON10</p></article>"
        "<article><h2>Travel offer 9%</h2><p>Code: DEMOR10</p></article></section>"
        + "".join(
            f"<article>Unrelated product {i}: ordinary catalog description.</article>"
            for i in range(200)
        )
        + "</body></html>"
    ).encode()
    saved = gateway.store.ingest(page)
    request = {
        "source": {"kind": "snapshot", "id": saved["snapshot_id"]},
        "subject": "Travel offer",
        "question": "What is the code for the 7% travel offer?",
        "answer_type": "exact_code",
        "qualifiers": {"discount": "7%"},
    }
    first, replay = gateway.resolve(request), gateway.resolve(request)
    changed_question = gateway.resolve(
        dict(request, question="Give the exact 7% travel offer code")
    )
    cert = first["certificate"]
    proposal = {
        "value": cert["value"],
        "evidence_ids": [e["id"] for e in cert["evidence"]],
    }
    accepted = gateway.verify(cert["certificate_id"], proposal)
    rejected = gateway.verify(cert["certificate_id"], dict(proposal, value="DEMOR10"))
    result = {
        "kind": "local_component_demonstration_not_agent_evaluation",
        "source_bytes": len(page),
        "certificate_bytes": len(encode(cert)),
        "replay_certificate_identical": cert == replay["certificate"],
        "different_question_reused_index": changed_question["usage"]["index_cache_hit"],
        "first_usage": first["usage"],
        "replay_usage": replay["usage"],
        "certificate": cert,
        "correct_answer_gate": accepted,
        "wrong_answer_gate": rejected,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
