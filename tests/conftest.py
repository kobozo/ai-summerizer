"""Contains global fixtures for unit tests."""

from pathlib import Path

import pytest

from ai_summerizer.models.settings import Settings


@pytest.fixture(autouse=True)
def setup_test_settings() -> None:
    """Set up test settings for all tests."""
    # Load test settings
    test_settings_path = Path(__file__).parent / "settings.json"
    Settings.from_json(test_settings_path)
