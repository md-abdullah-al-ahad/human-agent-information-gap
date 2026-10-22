"""Agent-visible MCP schemas. Runtime checks are also applied by the CLI/host."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SnapshotSource(StrictModel):
    kind: Literal["snapshot"]
    id: str = Field(
        pattern=r"^snapshot:[0-9a-f]{64}$",
        description="Handle returned by administrative registration",
    )


class LiveSource(StrictModel):
    kind: Literal["live"]
    url: str = Field(max_length=2048)
    render: Literal["http", "browser", "auto"] = "auto"


class Budget(StrictModel):
    max_wall_ms: int = Field(default=20000, ge=100, le=60000, strict=True)
    max_visual_regions: int = Field(default=3, ge=0, le=6, strict=True)
    max_ocr_calls: int = Field(default=4, ge=0, le=8, strict=True)
    max_vision_calls: int = Field(default=0, ge=0, le=1, strict=True)


class ResolveRequest(StrictModel):
    source: Annotated[SnapshotSource | LiveSource, Field(discriminator="kind")]
    answer_type: Literal[
        "exact_code",
        "exact_entity",
        "number",
        "date",
        "set",
        "instruction",
        "status",
        "quote",
    ]
    subject: str = Field(
        min_length=1,
        max_length=160,
        description="Exact entity or container label present in the source",
    )
    question: str = Field(default="", max_length=500)
    field: str = Field(
        default="", max_length=80, description="Source field label, e.g. Price or Name"
    )
    qualifiers: dict[str, str] = Field(default_factory=dict, max_length=6)
    scope: Literal["page", "data", "all_sources"] = "page"
    as_of: str = Field(
        default="capture",
        description="capture, current, or an ISO timestamp with timezone",
    )
    position: int | None = Field(default=None, ge=1, le=1000, strict=True)
    budget: Budget = Field(default_factory=Budget)
    evidence_ids: list[str] = Field(default_factory=list, max_length=3)
    compare_to: str | None = Field(default=None, pattern=r"^snapshot:[0-9a-f]{64}$")


class ProposedAnswer(StrictModel):
    value: str | list[str] | None
    evidence_ids: list[str] = Field(max_length=3)
