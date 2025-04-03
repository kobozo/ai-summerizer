"""Test cache decorator."""
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from ai_summerizer.helpers.decorators.cache import cache_content
from ai_summerizer.models.settings import Sources, YoutubeChannelSettings, YoutubeSettings
from ai_summerizer.models.source_content import SourceContent, SourceDetails
from ai_summerizer.sources.base import BaseSource


class TestSource(BaseSource):
    """Test source for cache decorator."""

    def __init__(self) -> None:
        """Initialize test source."""
        super().__init__(
            Sources(
                youtube=YoutubeSettings(
                    settings={"api_key": "test", "cache_duration": 3600},
                    channels=[
                        YoutubeChannelSettings(
                            id="test_id",
                            name="Test Channel",
                        ),
                    ],
                ),
            ),
        )

    @cache_content
    def get_content(self) -> SourceContent:
        """Get content from source."""
        return self._get_content()

    def _get_content(self) -> SourceContent:
        """Get content from source."""
        return SourceContent(
            source=SourceDetails(id="test_id", name="Test"),
            content="test content",
            date=datetime.now(timezone.utc),
        )


def test_cache_decorator(tmp_path: Path) -> None:
    """Test cache decorator."""
    # Use tmp_path as cache directory
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()

    # Create test source
    source = TestSource()

    # Patch the cache directory
    with patch("ai_summerizer.helpers.decorators.cache.Path") as mock_path:
        mock_path.return_value = cache_dir

        # First call should create cache
        content1 = source.get_content()
        assert content1.content == "test content"

        # Cache file should exist
        cache_file = cache_dir / "test_id.json"
        assert cache_file.exists()

        # Second call should use cache
        content2 = source.get_content()
        assert content2.content == "test content"
        assert content2.date == content1.date  # Dates should match if cached
