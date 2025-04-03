"""Run the main application."""

import logging
import sys

from ai_summerizer.main import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


def main_entry() -> None:
    """Run the main application."""
    main()
    sys.exit(0)


if __name__ == "__main__":
    main_entry()
