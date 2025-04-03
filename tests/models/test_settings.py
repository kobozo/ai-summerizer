"""Test settings models."""

import json
from pathlib import Path

from ai_summerizer.models.settings import (
    DEFAULT_CACHE_DURATION,
    Settings,
    Sources,
    YoutubeChannelSettings,
    YoutubeSettings,
    default_youtube_settings,
)


def test_default_youtube_settings() -> None:
    """Test default YouTube settings."""
    settings = default_youtube_settings()
    assert settings["api_key"] == ""
    assert settings["cache_duration"] == DEFAULT_CACHE_DURATION


def test_youtube_channel_settings() -> None:
    """Test YouTube channel settings."""
    channel = YoutubeChannelSettings(id="test_id", name="Test Channel")
    assert channel.id == "test_id"
    assert channel.name == "Test Channel"


def test_youtube_settings() -> None:
    """Test YouTube settings."""
    settings = YoutubeSettings()
    assert settings.settings["api_key"] == ""
    assert settings.settings["cache_duration"] == DEFAULT_CACHE_DURATION
    assert settings.channels == []


def test_sources() -> None:
    """Test sources."""
    sources = Sources()
    assert sources.youtube is None


def test_settings() -> None:
    """Test settings."""
    settings = Settings()
    assert settings.sources.youtube is None


def test_settings_from_json(tmp_path: Path) -> None:
    """Test loading settings from JSON."""
    # Create a test settings file
    settings_path = tmp_path / "test_settings.json"
    test_cache_duration = 3600  # 1 hour in seconds
    settings = Settings(
        sources=Sources(
            youtube=YoutubeSettings(
                settings={"api_key": "test", "cache_duration": test_cache_duration},
                channels=[
                    YoutubeChannelSettings(
                        id="test_id",
                        name="Test Channel",
                    ),
                ],
            ),
        ),
    )
    settings.save_to_json(settings_path)

    # Load the settings
    loaded_settings = Settings.from_json(settings_path)
    assert loaded_settings.sources.youtube is not None
    assert loaded_settings.sources.youtube.settings["api_key"] == "test"  # type: ignore[union-attr]
    assert loaded_settings.sources.youtube.settings["cache_duration"] == test_cache_duration  # type: ignore[union-attr]
    assert len(loaded_settings.sources.youtube.channels) == 1  # type: ignore[union-attr]
    assert loaded_settings.sources.youtube.channels[0].id == "test_id"  # type: ignore[union-attr]
    assert loaded_settings.sources.youtube.channels[0].name == "Test Channel"  # type: ignore[union-attr]


def test_settings_from_json_nonexistent() -> None:
    """Test loading settings from nonexistent JSON."""
    settings = Settings.from_json("nonexistent.json")
    assert settings.sources.youtube is None


def test_settings_save_to_json(tmp_path: Path) -> None:
    """Test saving settings to JSON."""
    settings_path = tmp_path / "test_settings.json"
    test_cache_duration = 3600  # 1 hour in seconds
    settings = Settings(
        sources=Sources(
            youtube=YoutubeSettings(
                settings={"api_key": "test", "cache_duration": test_cache_duration},
                channels=[
                    YoutubeChannelSettings(
                        id="test_id",
                        name="Test Channel",
                    ),
                ],
            ),
        ),
    )
    settings.save_to_json(settings_path)

    # Verify the file was created
    assert settings_path.exists()

    # Verify the contents
    with settings_path.open() as f:
        data = json.load(f)
        assert data["sources"]["youtube"]["settings"]["api_key"] == "test"
        assert data["sources"]["youtube"]["settings"]["cache_duration"] == test_cache_duration
        assert len(data["sources"]["youtube"]["channels"]) == 1
        assert data["sources"]["youtube"]["channels"][0]["id"] == "test_id"
        assert data["sources"]["youtube"]["channels"][0]["name"] == "Test Channel"
