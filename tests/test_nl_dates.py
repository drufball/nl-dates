"""Tests for the nl-dates library."""

from datetime import date

from nl_dates import calculate_date


def test_calculate_date_with_relative_date() -> None:
    """Test calculate_date with an explicit relative_to_date."""
    test_date = date(2025, 11, 18)
    result = calculate_date("tomorrow", relative_to_date=test_date)

    # Should return a date object
    assert isinstance(result, date)
    # The actual value will be determined by OpenAI
    assert result == date(2025, 11, 19)


def test_calculate_date_without_relative_date() -> None:
    """Test calculate_date defaults to current date when relative_to_date is None."""
    result = calculate_date("today")

    # Should return a date object
    assert isinstance(result, date)


def test_calculate_date_returns_date() -> None:
    """Test that calculate_date returns a date object."""
    test_date = date(2025, 1, 1)
    result = calculate_date("today", relative_to_date=test_date)

    # Should return a date object
    assert isinstance(result, date)
    assert result == test_date
