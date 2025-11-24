"""Natural language date parsing functionality."""

from datetime import date, datetime

from nl_dates.llm import LLMClient


def extract_date(
    task_description: str,
    relative_to_date: date | None = None,
    client: LLMClient | None = None,
) -> tuple[str, date | None]:
    """
    Extract date from a task description and return cleaned task with date.

    This function analyzes a task description that may contain natural language
    date references (like "tomorrow", "next Tuesday", etc.) and returns both
    a cleaned version of the task (with date references removed) and the
    extracted date as a date object.

    Args:
        task_description: Task description that may contain date information
            (e.g., "Submit report tomorrow", "Fix bug by next Tuesday")
        relative_to_date: Optional date to use as reference for relative dates.
            Defaults to current date.
        client: Optional LLM client to use for extraction. If None,
            a new client will be created using the OPENAI_API_KEY
            environment variable.

    Returns:
        Tuple of (cleaned_task, extracted_date) where:
        - cleaned_task (str): Task description with date content removed
        - extracted_date (date | None): Extracted date object, or None if no date found

    Examples:
        >>> extract_date("Submit report tomorrow")
        ('Submit report', datetime.date(2025, 11, 19))
        >>> extract_date("Fix the authentication bug")
        ('Fix the authentication bug', None)
        >>> extract_date("Deploy by next Tuesday", relative_to_date=date(2025, 1, 1))
        ('Deploy', datetime.date(2025, 1, 7))

    Raises:
        ValueError: If the LLM fails to process the request or API key is not set
    """
    if relative_to_date is None:
        relative_to_date = datetime.now().date()

    # Create client if not provided (dependency injection)
    if client is None:
        client = LLMClient()

    # Extract date and cleaned task using the LLM client
    cleaned_task, date_str = client.extract_date_from_task(
        task_description, relative_to_date
    )

    # If no date was found, return None for the date
    if date_str is None:
        return (cleaned_task, None)

    try:
        # Parse the ISO date string
        parsed_date = date.fromisoformat(date_str)
        return (cleaned_task, parsed_date)
    except ValueError as e:
        raise ValueError(
            f"Failed to parse date from task '{task_description}': "
            f"LLM returned invalid ISO date '{date_str}'"
        ) from e
