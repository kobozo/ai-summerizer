"""Tests for models package."""
from datetime import datetime, timezone

from ai_summerizer.models.source_content import SourceContent, SourceDetails


def test_source_content_model() -> None:
    """Test SourceContent model creation and validation."""
    test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    source_details = SourceDetails(type="test", details="test details")
    content = SourceContent(
        source=source_details,
        content="test content",
        date=test_date,
    )

    assert content.source.type == "test"
    assert content.source.details == "test details"
    assert content.content == "test content"
    assert content.date == test_date

    # Test optional date
    content_no_date = SourceContent(
        source=source_details,
        content="test content",
    )
    assert content_no_date.date is None
