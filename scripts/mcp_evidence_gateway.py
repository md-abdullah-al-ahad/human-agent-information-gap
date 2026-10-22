"""LWA-Web v2 MCP server. Only registered snapshots are accessible by default."""

from __future__ import annotations

import json

from fastmcp import FastMCP
from fastmcp.utilities.types import Image

try:
    from .evidence_gateway.gateway import Gateway
    from .evidence_gateway.schemas import ProposedAnswer, ResolveRequest
except ImportError:
    from evidence_gateway.gateway import Gateway
    from evidence_gateway.schemas import ProposedAnswer, ResolveRequest


def create_server(gateway=None):
    gateway = gateway or Gateway()
    server = FastMCP("lwa-evidence-gateway-v2")

    @server.tool()
    def resolve_evidence(request: ResolveRequest) -> dict:
        """Return a compact evidence certificate for a typed question.

        Required: source={kind:'snapshot',id:'snapshot:...'}, answer_type,
        subject (an exact entity/container label). Optional: question, field,
        qualifiers, scope ('page'/'data'/'all_sources'), as_of ('capture'/'current'
        or ISO timestamp), position, evidence_ids, compare_to (snapshot handle), budget. Answer types:
        exact_code, exact_entity, number, date, set, instruction, status, quote.
        Number/entity extraction benefits from an explicit field label.
        Live URL sources work only if the server administrator enabled live mode.
        Ambiguity and absence from inspected scope are never evidence of global absence.
        """
        return gateway.resolve(request.model_dump(exclude_none=True))

    @server.tool()
    def inspect_evidence(evidence_id: str, view: str = "text") -> list:
        """Read one bounded source excerpt or saved crop; view is 'text' or 'crop'."""
        metadata, pixels = gateway.inspect(evidence_id, view)
        result = [json.dumps(metadata, ensure_ascii=False)]
        if pixels:
            result.append(Image(data=pixels, format="png"))
        return result

    @server.tool()
    def verify_answer(certificate_id: str, proposed_answer: ProposedAnswer) -> dict:
        """Gate an exact answer: proposed_answer={value:...,evidence_ids:[...]}.

        Reject mismatched codes, names, missing instruction steps, added free
        prose, uncertain certificates, and incorrect citations. Returns a final
        answer artifact only if the configured evidence policy permits it.
        """
        return gateway.verify(certificate_id, proposed_answer.model_dump())

    return server


if __name__ == "__main__":
    create_server().run()
