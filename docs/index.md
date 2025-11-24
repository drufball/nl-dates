# nl-dates Documentation

Extract dates from task descriptions and return cleaned tasks using OpenAI's GPT-4.

## Installation

```bash
# Using uv
uv add git+https://github.com/drufball/nl-dates.git

# Using pip
pip install git+https://github.com/drufball/nl-dates.git
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

## Quick Start

```python
from nl_dates import extract_date

# Extract date from task description
task, date = extract_date("Submit report tomorrow")
# task: "Submit report"
# date: date(2025, 11, 19)

# Task without date returns None
task, date = extract_date("Fix the authentication bug")
# task: "Fix the authentication bug"
# date: None

# With a reference date
from datetime import date
task, date_obj = extract_date(
    "Review code by next Tuesday",
    relative_to_date=date(2025, 1, 1)
)
# task: "Review code"
# date_obj: date(2025, 1, 7)
```

## API Reference

### `extract_date(task_description, relative_to_date=None, client=None)`

Extracts date information from a task description and returns the cleaned task with the extracted date.

**Parameters:**
- `task_description` (str): Task description that may contain natural language dates (e.g., "Submit report tomorrow", "Fix bug by next Tuesday")
- `relative_to_date` (date, optional): Reference date for relative parsing. Defaults to today
- `client` (LLMClient, optional): Custom LLM client. Defaults to creating one with `OPENAI_API_KEY`

**Returns:** Tuple of `(cleaned_task, extracted_date)`
- `cleaned_task` (str): Task description with date content removed
- `extracted_date` (date | None): Extracted date object, or None if no date found

**Raises:** `ValueError` if LLM processing fails or API key is missing

### Supported Date Formats

The library can extract various natural language date formats from task descriptions:

- Relative: "tomorrow", "yesterday", "today"
- Day of week: "next Monday", "this Friday", "last Tuesday"
- Relative periods: "in 3 days", "2 weeks ago", "next month"
- Specific dates: "January 1st", "March 15, 2025"
- Prepositional phrases: "by Friday", "on Monday", "before next week"

## Advanced Usage

### Reuse Client for Multiple Calls

```python
from nl_dates.llm import LLMClient

client = LLMClient()
tasks = ["Submit report tomorrow", "Review code by Friday", "Fix bug"]
results = [extract_date(t, client=client) for t in tasks]
```

### Custom API Key

```python
from nl_dates.llm import LLMClient

client = LLMClient(api_key="your-api-key")
task, date = extract_date("Deploy next week", client=client)
```

### Working with Results

```python
task, extracted_date = extract_date("Complete project by tomorrow")

# Check if date was found
if extracted_date:
    print(f"Task: {task}")
    print(f"Due: {extracted_date.isoformat()}")
else:
    print(f"No deadline: {task}")
```

## Requirements

- Python >= 3.13
- OpenAI API key

