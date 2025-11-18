"""LLM client for natural language date parsing."""

import os
from datetime import date

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


class LLMClient:
    """Client for interacting with LLM to parse natural language dates."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the LLM client.

        Args:
            api_key: OpenAI API key. If None, will try to load from
                OPENAI_API_KEY environment variable.

        Raises:
            ValueError: If API key is not provided and not found in environment.
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable must be set or "
                "api_key must be provided"
            )
        self.client = OpenAI(api_key=api_key)

    def parse_date(self, date_string: str, relative_to_date: date) -> str:
        """
        Parse a natural language date string to ISO 8601 format using LLM.

        Args:
            date_string: Natural language description of a date
                (e.g., "tomorrow", "next Tuesday")
            relative_to_date: Date to use as reference for relative dates

        Returns:
            ISO 8601 formatted date string (YYYY-MM-DD)

        Raises:
            ValueError: If the LLM fails to parse the date or returns invalid response
        """
        prompt = f"""Parse the following natural language date string into \
an ISO 8601 date format (YYYY-MM-DD).

Natural language date: "{date_string}"
Reference date (today): {relative_to_date.isoformat()}

Return ONLY the parsed date in ISO 8601 format (YYYY-MM-DD), \
nothing else. Do not include time.

Examples:
- "tomorrow" relative to 2025-11-18 → 2025-11-19
- "next Tuesday" relative to 2025-11-18 → 2025-11-19
- "today" relative to 2025-01-01 → 2025-01-01
- "in 3 days" relative to 2025-11-18 → 2025-11-21"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )

            response_content = response.choices[0].message.content
            if not response_content:
                raise ValueError("OpenAI API returned empty response")

            return response_content.strip()

        except Exception as e:
            raise ValueError(
                f"Failed to parse date string '{date_string}': {e!s}"
            ) from e
