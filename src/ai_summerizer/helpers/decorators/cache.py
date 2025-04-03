"""Cache decorator for source content."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Callable, TypeVar, cast

if TYPE_CHECKING:
    from ai_summerizer.models.source_content import SourceContent
    from ai_summerizer.sources.base import BaseSource

T = TypeVar("T", bound="BaseSource")


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects."""

    def default(self, obj: datetime) -> str:
        """Convert datetime objects to ISO format strings."""
        return obj.isoformat()


def cache_content(func: Callable[[T], SourceContent]) -> Callable[[T], SourceContent]:
    """
    Cache source content based on source ID.

    Args:
        func: The function to cache.

    Returns:
        The wrapped function.

    """

    @wraps(func)
    def wrapper(self: T) -> SourceContent:
        # Get source ID and cache duration from settings
        source_id = self.sources.youtube.channels[0].id  # type: ignore[union-attr]
        cache_duration = cast(float, self.sources.youtube.settings["cache_duration"])  # type: ignore[union-attr]

        # Create cache directory if it doesn't exist
        cache_dir = Path(".cache")
        cache_dir.mkdir(exist_ok=True)

        # Create cache file path
        cache_file = cache_dir / f"{source_id}.json"

        # Check if cache exists and is still valid
        if cache_file.exists():
            with cache_file.open("r") as f:
                cache_data = json.load(f)
                cached_time = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now(timezone.utc) - cached_time < timedelta(seconds=cache_duration):
                    # Cache is still valid, return cached content
                    from ai_summerizer.models.source_content import SourceContent
                    return SourceContent.model_validate(cache_data["content"])

        # Cache miss or expired, call original function
        content = func(self)

        # Save to cache
        cache_data = {
            "timestamp": datetime.now(timezone.utc),
            "content": content.model_dump(),
        }
        with cache_file.open("w") as f:
            json.dump(cache_data, f, cls=DateTimeEncoder)

        return content

    return wrapper
