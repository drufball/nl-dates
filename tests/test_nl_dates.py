"""Tests for the nl-dates library."""

from datetime import date
from unittest.mock import MagicMock

import pytest

from nl_dates import extract_date
from nl_dates.llm import LLMClient


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """Create a mock LLM client for testing."""
    return MagicMock(spec=LLMClient)


def test_extract_date_with_date_in_task(mock_llm_client: MagicMock) -> None:
    """Test extract_date with a task containing a date."""
    test_date = date(2025, 11, 18)

    # Mock the LLM to return cleaned task and ISO date
    mock_llm_client.extract_date_from_task.return_value = (
        "Submit report",
        "2025-11-19",
    )

    cleaned_task, extracted_date = extract_date(
        "Submit report tomorrow", relative_to_date=test_date, client=mock_llm_client
    )

    # Verify the mock was called with correct arguments
    mock_llm_client.extract_date_from_task.assert_called_once_with(
        "Submit report tomorrow", test_date
    )

    # Should return cleaned task and date object
    assert cleaned_task == "Submit report"
    assert isinstance(extracted_date, date)
    assert extracted_date == date(2025, 11, 19)


def test_extract_date_without_date_in_task(mock_llm_client: MagicMock) -> None:
    """Test extract_date with a task containing no date."""
    test_date = date(2025, 11, 18)

    # Mock the LLM to return cleaned task and None for date
    mock_llm_client.extract_date_from_task.return_value = (
        "Fix the authentication bug",
        None,
    )

    cleaned_task, extracted_date = extract_date(
        "Fix the authentication bug",
        relative_to_date=test_date,
        client=mock_llm_client,
    )

    # Verify the mock was called with correct arguments
    mock_llm_client.extract_date_from_task.assert_called_once_with(
        "Fix the authentication bug", test_date
    )

    # Should return cleaned task and None for date
    assert cleaned_task == "Fix the authentication bug"
    assert extracted_date is None


def test_extract_date_defaults_to_current_date(mock_llm_client: MagicMock) -> None:
    """Test extract_date defaults to current date when relative_to_date is None."""
    # Mock the LLM to return a cleaned task and date
    mock_llm_client.extract_date_from_task.return_value = ("Deploy", "2025-11-21")

    cleaned_task, extracted_date = extract_date(
        "Deploy in 3 days", client=mock_llm_client
    )

    # Should return cleaned task and date object
    assert cleaned_task == "Deploy"
    assert isinstance(extracted_date, date)

    # Verify the mock was called
    mock_llm_client.extract_date_from_task.assert_called_once()


def test_extract_date_with_complex_task(mock_llm_client: MagicMock) -> None:
    """Test extract_date with a more complex task description."""
    test_date = date(2025, 1, 1)

    # Mock the LLM to return cleaned task and date
    mock_llm_client.extract_date_from_task.return_value = (
        "Review code",
        "2025-01-07",
    )

    cleaned_task, extracted_date = extract_date(
        "Review code by next Tuesday",
        relative_to_date=test_date,
        client=mock_llm_client,
    )

    # Should return cleaned task and date object
    assert cleaned_task == "Review code"
    assert isinstance(extracted_date, date)
    assert extracted_date == date(2025, 1, 7)


def test_extract_date_invalid_llm_response(mock_llm_client: MagicMock) -> None:
    """Test that extract_date handles invalid LLM responses."""
    test_date = date(2025, 11, 18)

    # Mock the LLM to return an invalid ISO date
    mock_llm_client.extract_date_from_task.return_value = (
        "Submit report",
        "not-a-date",
    )

    with pytest.raises(ValueError, match="LLM returned invalid ISO date"):
        extract_date(
            "Submit report tomorrow",
            relative_to_date=test_date,
            client=mock_llm_client,
        )


def test_extract_date_llm_error(mock_llm_client: MagicMock) -> None:
    """Test that extract_date handles LLM errors."""
    test_date = date(2025, 11, 18)

    # Mock the LLM to raise an error
    mock_llm_client.extract_date_from_task.side_effect = ValueError("LLM API error")

    with pytest.raises(ValueError, match="LLM API error"):
        extract_date(
            "Submit report tomorrow",
            relative_to_date=test_date,
            client=mock_llm_client,
        )
