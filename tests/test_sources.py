"""Tests for sources package."""
from datetime import datetime, timezone

from ai_summerizer.models.source_content import SourceContent, SourceDetails
from ai_summerizer.sources.base import BaseSource


class TestSource(BaseSource):
    """Test implementation of BaseSource."""

    def _get_content(self) -> SourceContent:
        """Return test content."""
        test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        return SourceContent(
            source=SourceDetails(type="test", details="test details"),
            content="test content",
            date=test_date,
        )


def test_base_source() -> None:
    """Test BaseSource implementation."""
    config = {"test_key": "test_value"}
    source = TestSource(config)

    assert source.config == config

    content = source.get_content()
    test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)

    assert isinstance(content, SourceContent)
    assert content.source.type == "test"
    assert content.source.details == "test details"
    assert content.content == "test content"
    assert content.date == test_date
