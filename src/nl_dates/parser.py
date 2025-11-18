"""Natural language date parsing functionality."""

from datetime import date, datetime

from nl_dates.llm import get_default_client


def calculate_date(date_string: str, relative_to_date: date | None = None) -> date:
    """
    Convert a natural language date string to a date object using OpenAI.

    Args:
        date_string: Natural language description of a date
            (e.g., "tomorrow", "next Tuesday")
        relative_to_date: Optional date to use as reference.
            Defaults to current date.

    Returns:
        date object representing the parsed date

    Examples:
        >>> calculate_date("tomorrow")
        datetime.date(2025, 11, 19)
        >>> calculate_date("today", relative_to_date=date(2025, 1, 1))
        datetime.date(2025, 1, 1)

    Raises:
        ValueError: If the date string cannot be parsed or API key is not set
    """
    if relative_to_date is None:
        relative_to_date = datetime.now().date()

    # Get the LLM client and parse the date
    client = get_default_client()
    response_text = client.parse_date(date_string, relative_to_date)

    try:
        # Parse the ISO date string
        parsed_date = date.fromisoformat(response_text)
        return parsed_date
    except ValueError as e:
        raise ValueError(
            f"Failed to parse date string '{date_string}': "
            f"LLM returned invalid ISO date '{response_text}'"
        ) from e
