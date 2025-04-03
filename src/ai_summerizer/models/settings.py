"""Settings models for the application."""
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

# Constants
DEFAULT_CACHE_DURATION = 86400  # 24 hours in seconds


def default_youtube_settings() -> dict[str, str | int]:
    """
    Get default YouTube settings.

    Returns:
        Default YouTube settings.

    """
    return {
        "api_key": "",
        "cache_duration": DEFAULT_CACHE_DURATION,
    }


class YoutubeChannelSettings(BaseModel):
    """Settings for a YouTube channel."""

    id: str
    name: str


class YoutubeSettings(BaseModel):
    """Settings for YouTube source."""

    settings: dict[str, str | int] = Field(default_factory=default_youtube_settings)
    channels: list[YoutubeChannelSettings] = Field(default_factory=list)


class Sources(BaseModel):
    """Settings for sources."""

    youtube: YoutubeSettings | None = None


class Settings(BaseModel):
    """Application settings."""

    sources: Sources = Field(default_factory=Sources)

    @classmethod
    def from_json(cls, file_path: str | Path) -> Settings:
        """
        Load settings from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            Settings instance.

        """
        file_path = Path(file_path)
        if not file_path.exists():
            return cls()

        with file_path.open() as f:
            data = json.load(f)
            return cls.model_validate(data)

    def save_to_json(self, file_path: str | Path) -> None:
        """
        Save settings to a JSON file.

        Args:
            file_path: Path to save the JSON file.

        """
        with Path(file_path).open("w") as f:
            json.dump(self.model_dump(), f, indent=2)


# Create a single instance of the settings
settings = Settings.from_json("settings.json")
