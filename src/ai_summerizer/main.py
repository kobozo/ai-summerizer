"""Flask application endpoints for AI Summerizer API."""

from __future__ import annotations

import logging

from ai_summerizer.core.process_sources import process_sources
from ai_summerizer.models.settings import settings

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the application."""
    contents = process_sources(settings)
    for content in contents:
        logger.info(content)


if __name__ == "__main__":
    main()
