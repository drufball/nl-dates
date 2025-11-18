"""Tests for the nl-dates library."""

from datetime import datetime

from nl_dates import calculate_date


def test_calculate_date_with_relative_date() -> None:
    """Test calculate_date with an explicit relative_to_date."""
    test_date = datetime(2025, 11, 18, 12, 30, 45)
    result = calculate_date("tomorrow", relative_to_date=test_date)

    # For now, it just returns the relative date
    assert result == test_date
    assert isinstance(result, datetime)


def test_calculate_date_without_relative_date() -> None:
    """Test calculate_date defaults to current datetime when relative_to_date is None."""
    result = calculate_date("today")

    # Should return a datetime object
    assert isinstance(result, datetime)


def test_calculate_date_returns_datetime() -> None:
    """Test that calculate_date returns a datetime object."""
    test_date = datetime(2025, 1, 1, 0, 0, 0)
    result = calculate_date("any string", relative_to_date=test_date)

    # Should return a datetime object
    assert isinstance(result, datetime)
    assert result == test_date
