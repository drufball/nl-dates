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

    def extract_date_from_task(
        self, task_description: str, relative_to_date: date
    ) -> tuple[str, str | None]:
        """
        Extract date information from a task description and return cleaned task.

        Args:
            task_description: Task description that may contain natural language dates
            relative_to_date: Date to use as reference for relative dates

        Returns:
            Tuple of (cleaned_task_description, iso_date_or_none)
            - cleaned_task_description: Task with date content removed
            - iso_date_or_none: ISO 8601 date (YYYY-MM-DD) if found, None otherwise

        Raises:
            ValueError: If the LLM fails to process the request
        """
        prompt = f"""Analyze the following task description and extract any date \
information.

Task description: "{task_description}"
Reference date (today): {relative_to_date.isoformat()}

Your response must be EXACTLY two lines:
1. First line: The task description with any date-related content removed
2. Second line: Either the ISO 8601 date (YYYY-MM-DD) if a date is \
mentioned, or the word "None" if no date is found

Examples:
Input: "Submit report tomorrow"
Output:
Submit report
2025-11-19

Input: "Review code by next Tuesday"
Output:
Review code
2025-11-19

Input: "Fix the authentication bug"
Output:
Fix the authentication bug
None

Input: "Deploy in 3 days"
Output:
Deploy
2025-11-21"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}],
            )

            response_content = response.choices[0].message.content
            if not response_content:
                raise ValueError("OpenAI API returned empty response")

            lines = response_content.strip().split("\n")
            if len(lines) < 2:
                raise ValueError(
                    f"Expected 2 lines in response, got {len(lines)}: "
                    f"{response_content}"
                )

            cleaned_task = lines[0].strip()
            date_str = lines[1].strip()

            # Return None if the LLM indicated no date was found
            if date_str.lower() == "none":
                return (cleaned_task, None)

            return (cleaned_task, date_str)

        except Exception as e:
            raise ValueError(
                f"Failed to extract date from task '{task_description}': {e!s}"
            ) from e
