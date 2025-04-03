"""Test settings models."""
from ai_summerizer.models.settings import (
    DEFAULT_CACHE_DURATION,
    BaseSourceSettings,
    Settings,
    Sources,
    YoutubeChannelSettings,
    YoutubeSettings,
)


def test_base_source_settings() -> None:
    """Test base source settings."""
    settings = BaseSourceSettings(
        id="@test",
        name="Test Source",
    )

    assert settings.enabled is True
    assert settings.id == "@test"
    assert settings.name == "Test Source"
    assert settings.type == "user"


def test_youtube_channel_settings() -> None:
    """Test YouTube channel settings inheritance."""
    settings = YoutubeChannelSettings(
        id="@test",
        name="Test Channel",
        type="channel",
        time_period="2d",
    )

    # Base settings
    assert settings.enabled is True
    assert settings.id == "@test"
    assert settings.name == "Test Channel"
    assert settings.type == "channel"

    # YouTube specific settings
    assert settings.time_period == "2d"


def test_settings_model() -> None:
    """Test settings model creation and validation."""
    settings = Settings(
        sources=Sources(
            youtube=YoutubeSettings(
                settings={
                    "api_key": "test_key",
                    "cache_duration": DEFAULT_CACHE_DURATION,
                },
                channels=[
                    YoutubeChannelSettings(
                        enabled=True,
                        id="@test",
                        name="Test Channel",
                        type="user",
                        time_period="1d",
                    ),
                ],
            ),
        ),
    )

    assert settings.sources.youtube is not None
    assert settings.sources.youtube.settings["api_key"] == "test_key"
    assert settings.sources.youtube.settings["cache_duration"] == DEFAULT_CACHE_DURATION
    assert len(settings.sources.youtube.channels) == 1
    assert settings.sources.youtube.channels[0].id == "@test"
    assert settings.sources.youtube.channels[0].name == "Test Channel"


def test_settings_model_defaults() -> None:
    """Test settings model defaults."""
    settings = Settings()

    assert settings.sources.youtube is None


def test_settings_model_no_youtube() -> None:
    """Test settings model with no YouTube configuration."""
    settings = Settings(sources=Sources())

    assert settings.sources.youtube is None
