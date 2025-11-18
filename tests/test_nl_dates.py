"""Tests for the nl-dates library."""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from nl_dates import calculate_date
from nl_dates.llm import LLMClient, set_default_client


@pytest.fixture
def mock_llm_client() -> LLMClient:
    """Create a mock LLM client for testing."""
    mock_client = MagicMock(spec=LLMClient)
    set_default_client(mock_client)
    return mock_client


@pytest.fixture(autouse=True)
def _reset_default_client() -> None:
    """Reset the default client after each test."""
    yield
    set_default_client(None)


def test_calculate_date_with_relative_date(mock_llm_client: LLMClient) -> None:
    """Test calculate_date with an explicit relative_to_date."""
    test_date = date(2025, 11, 18)
    
    # Mock the LLM to return a specific ISO date
    mock_llm_client.parse_date.return_value = "2025-11-19"
    
    result = calculate_date("tomorrow", relative_to_date=test_date)

    # Verify the mock was called with correct arguments
    mock_llm_client.parse_date.assert_called_once_with("tomorrow", test_date)
    
    # Should return a date object
    assert isinstance(result, date)
    assert result == date(2025, 11, 19)


def test_calculate_date_without_relative_date(mock_llm_client: LLMClient) -> None:
    """Test calculate_date defaults to current date when relative_to_date is None."""
    # Mock the LLM to return today's date (whatever it is)
    mock_llm_client.parse_date.return_value = "2025-11-18"
    
    result = calculate_date("today")

    # Should return a date object
    assert isinstance(result, date)
    
    # Verify the mock was called
    mock_llm_client.parse_date.assert_called_once()


def test_calculate_date_returns_date(mock_llm_client: LLMClient) -> None:
    """Test that calculate_date returns a date object."""
    test_date = date(2025, 1, 1)
    
    # Mock the LLM to return the same date
    mock_llm_client.parse_date.return_value = "2025-01-01"
    
    result = calculate_date("today", relative_to_date=test_date)

    # Should return a date object
    assert isinstance(result, date)
    assert result == test_date


def test_calculate_date_invalid_llm_response(mock_llm_client: LLMClient) -> None:
    """Test that calculate_date handles invalid LLM responses."""
    test_date = date(2025, 11, 18)
    
    # Mock the LLM to return an invalid ISO date
    mock_llm_client.parse_date.return_value = "not-a-date"
    
    with pytest.raises(ValueError, match="LLM returned invalid ISO date"):
        calculate_date("tomorrow", relative_to_date=test_date)


def test_calculate_date_llm_error(mock_llm_client: LLMClient) -> None:
    """Test that calculate_date handles LLM errors."""
    test_date = date(2025, 11, 18)
    
    # Mock the LLM to raise an error
    mock_llm_client.parse_date.side_effect = ValueError("LLM API error")
    
    with pytest.raises(ValueError, match="LLM API error"):
        calculate_date("tomorrow", relative_to_date=test_date)
