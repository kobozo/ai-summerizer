"""Base class for content sources."""
from abc import ABC, abstractmethod
from typing import Any

from ai_summerizer.models.source_content import SourceContent


class BaseSource(ABC):
    """Abstract base class for all content sources."""

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the source with its configuration.

        Args:
            config: Source-specific configuration dictionary

        """
        self.config = config

    def get_content(self) -> SourceContent:
        """
        Get standardized content from the source.

        This method implements the template pattern, where the actual content
        retrieval is delegated to the abstract _get_content method.

        Returns:
            SourceContent: Standardized content object

        """
        return self._get_content()

    @abstractmethod
    def _get_content(self) -> SourceContent:
        """
        Abstract method to be implemented by concrete sources.

        Returns:
            SourceContent: Standardized content object

        """
