"""Test YouTube source implementation."""
from datetime import datetime, timezone

from ai_summerizer.models.settings import Sources, YoutubeChannelSettings, YoutubeSettings
from ai_summerizer.sources.youtube import YouTubeSource


def test_youtube_source() -> None:
    """Test YouTube source implementation."""
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
    source = YouTubeSource(sources)

    content = source.get_content()
    assert content.source.id == "test_id"
    assert content.source.name == "Test Channel"
    assert content.content == "Demo YouTube content"
    assert isinstance(content.date, datetime)
    assert content.date.tzinfo == timezone.utc
