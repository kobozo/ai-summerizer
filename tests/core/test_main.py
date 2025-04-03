"""Test main module."""

from unittest.mock import patch

from ai_summerizer.__main__ import main_entry


def test_main_entry() -> None:
    """Test main entry point."""
    with patch("sys.exit") as mock_exit:
        main_entry()
        mock_exit.assert_called_once_with(0)
