"""Test process_sources implementation."""

from ai_summerizer.core.process_sources import process_sources
from ai_summerizer.models.settings import Settings, Sources, YoutubeChannelSettings, YoutubeSettings


def test_process_sources() -> None:
    """Test process_sources implementation."""
    settings = Settings(
        sources=Sources(
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

    contents = process_sources(settings)
    assert len(contents) == 1
    assert contents[0] == "Demo YouTube content"


def test_process_sources_no_youtube() -> None:
    """Test process_sources implementation with no YouTube source."""
    settings = Settings(
        sources=Sources(
            youtube=None,
        ),
    )

    contents = process_sources(settings)
    assert len(contents) == 0
