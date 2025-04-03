"""Process sources and return their content."""

import logging

from ai_summerizer.models.settings import Settings
from ai_summerizer.sources.youtube import YouTubeSource

logger = logging.getLogger(__name__)


def process_sources(settings: Settings) -> list[str]:
    """
    Process all enabled sources and return their content.

    Args:
        settings: Settings instance.

    Returns:
        List of content strings.

    """
    contents: list[str] = []

    # Process YouTube source if enabled
    if settings.sources.youtube is not None:
        logger.info("Processing YouTube source: %s", settings.sources.youtube.channels[0].name)
        youtube = YouTubeSource(settings.sources)
        content = youtube.get_content()
        contents.append(content.content)

    return contents
