"""Test main function module."""

import logging

import pytest

from ai_summerizer.main import main
from ai_summerizer.models.settings import Settings, Sources, YoutubeChannelSettings, YoutubeSettings


def test_main(caplog: pytest.LogCaptureFixture) -> None:
    """Test main function."""
    # Set up test settings
    Settings.settings = Settings(
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

    with caplog.at_level(logging.INFO):
        main()
        assert "Demo YouTube content" in caplog.text
