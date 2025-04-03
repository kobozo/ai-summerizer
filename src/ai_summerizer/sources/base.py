"""Base source class for content retrieval."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ai_summerizer.helpers.decorators.cache import cache_content

if TYPE_CHECKING:
    from ai_summerizer.models.settings import Sources
    from ai_summerizer.models.source_content import SourceContent


class BaseSource(ABC):
    """Base class for all content sources."""

    def __init__(self, sources: Sources) -> None:
        """
        Initialize source with configuration.

        Args:
            sources: Sources configuration containing settings for all sources.

        """
        self.sources = sources

    @cache_content
    def get_content(self) -> SourceContent:
        """
        Get content from source with standardized output.

        Returns:
            SourceContent: Standardized content output.

        """
        return self._get_content()

    @abstractmethod
    def _get_content(self) -> SourceContent:
        """
        Implement source-specific content retrieval.

        Returns:
            SourceContent: Standardized content output.

        """
