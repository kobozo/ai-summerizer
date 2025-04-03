"""Models for standardized source content output."""
from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict


class SourceDetails(BaseModel):
    """Details about the source of the content."""

    type: str
    details: str


class SourceContent(BaseModel):
    """Standardized content output from any source."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: SourceDetails
    content: str
    date: datetime | None = None


# Rebuild models to ensure datetime is properly defined
SourceContent.model_rebuild()
