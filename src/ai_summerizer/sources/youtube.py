"""YouTube source implementation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from ai_summerizer.models.source_content import SourceContent, SourceDetails
from ai_summerizer.sources.base import BaseSource

if TYPE_CHECKING:
    from ai_summerizer.models.settings import Sources


class YouTubeSource(BaseSource):
    """YouTube source implementation."""

    def __init__(self, sources: Sources) -> None:
        """Initialize YouTube source."""
        super().__init__(sources)

    def _get_content(self) -> SourceContent:
        """Get content from YouTube."""
        # Demo implementation
        return SourceContent(
            source=SourceDetails(
                id=self.sources.youtube.channels[0].id,  # type: ignore[union-attr]
                name=self.sources.youtube.channels[0].name,  # type: ignore[union-attr]
            ),
            content="Demo YouTube content",
            date=datetime.now(timezone.utc),
        )
