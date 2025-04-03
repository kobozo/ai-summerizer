"""Test source implementations."""
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from ai_summerizer.models.settings import Sources, YoutubeChannelSettings, YoutubeSettings
from ai_summerizer.models.source_content import SourceContent, SourceDetails
from ai_summerizer.sources.base import BaseSource


class TestSource(BaseSource):
    """Test source implementation."""

    def _get_content(self) -> SourceContent:
        """Get test content."""
        return SourceContent(
            source=SourceDetails(id="test_id", name="Test"),
            content="test content",
            date=datetime.now(timezone.utc),
        )


def test_base_source(tmp_path: Path) -> None:
    """Test BaseSource implementation."""
    # Use tmp_path as cache directory
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()

    sources = Sources(
        youtube=YoutubeSettings(
            settings={"api_key": "test", "cache_duration": 3600},
            channels=[
                YoutubeChannelSettings(
                    id="test_id",
                    name="Test Channel",
                ),
            ],
        ),
    )
    source = TestSource(sources)

    assert source.sources == sources

    # Patch the cache directory
    with patch("ai_summerizer.helpers.decorators.cache.Path") as mock_path:
        mock_path.return_value = cache_dir

        content = source.get_content()
        assert content.source.id == "test_id"
        assert content.source.name == "Test"
        assert content.content == "test content"
        assert content.date is not None
