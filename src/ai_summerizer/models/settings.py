"""Models for application settings."""
from __future__ import annotations

from pydantic import BaseModel, Field

# Constants
DEFAULT_CACHE_DURATION = 86400  # 24 hours in seconds


class YoutubeChannelSettings(BaseModel):
    """Settings for a YouTube channel."""

    enabled: bool = True
    id: str
    name: str
    type: str = "user"
    time_period: str = "1d"


class YoutubeSettings(BaseModel):
    """Settings for YouTube source."""

    settings: dict[str, str | int] = Field(
        default_factory=lambda: {
            "api_key": "",
            "cache_duration": DEFAULT_CACHE_DURATION,
        },
    )
    channels: list[YoutubeChannelSettings] = Field(default_factory=list)


class Sources(BaseModel):
    """Sources configuration."""

    youtube: YoutubeSettings | None = Field(default=None)


class Settings(BaseModel):
    """Application settings."""

    sources: Sources = Field(default_factory=Sources)
