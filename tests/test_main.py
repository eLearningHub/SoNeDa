"""Test cases for the __main__ module."""

from soneda.cli import app


def test_main_succeeds() -> None:
    """It exits with a status code of zero."""
    result = app()
    assert result.exit_code == 0
