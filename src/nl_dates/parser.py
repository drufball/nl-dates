"""Natural language date parsing functionality."""

import os
from datetime import date, datetime

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


def calculate_date(date_string: str, relative_to_date: date | None = None) -> date:
    """
    Convert a natural language date string to a date object using OpenAI.

    Args:
        date_string: Natural language description of a date (e.g., "tomorrow", "next Tuesday")
        relative_to_date: Optional date to use as reference. Defaults to current date.

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

    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set to use this function"
        )

    client = OpenAI(api_key=api_key)

    # Create the prompt for OpenAI
    prompt = f"""Parse the following natural language date string into an ISO 8601 date format (YYYY-MM-DD).

Natural language date: "{date_string}"
Reference date (today): {relative_to_date.isoformat()}

Return ONLY the parsed date in ISO 8601 format (YYYY-MM-DD), nothing else. Do not include time.

Examples:
- "tomorrow" relative to 2025-11-18 → 2025-11-19
- "next Tuesday" relative to 2025-11-18 → 2025-11-19
- "today" relative to 2025-01-01 → 2025-01-01
- "in 3 days" relative to 2025-11-18 → 2025-11-21"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Parse the ISO date string
        parsed_date = date.fromisoformat(response_text)

        return parsed_date

    except Exception as e:
        raise ValueError(
            f"Failed to parse date string '{date_string}': {str(e)}"
        ) from e
