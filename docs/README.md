# nl-dates Documentation

Convert natural language date strings into ISO date format using OpenAI's GPT-4.

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
from nl_dates import calculate_date

# Basic usage
calculate_date("tomorrow")  # date(2025, 11, 19)
calculate_date("next Tuesday")  # date(2025, 11, 19)
calculate_date("in 3 days")  # date(2025, 11, 21)

# With a reference date
from datetime import date
calculate_date("next week", relative_to_date=date(2025, 1, 1))

# Convert to ISO format
calculate_date("tomorrow").isoformat()  # '2025-11-19'
```

## API Reference

### `calculate_date(date_string, relative_to_date=None, client=None)`

Converts a natural language date string to a `date` object.

**Parameters:**
- `date_string` (str): Natural language date like "tomorrow", "next Tuesday", "in 3 days"
- `relative_to_date` (date, optional): Reference date for relative parsing. Defaults to today
- `client` (LLMClient, optional): Custom LLM client. Defaults to creating one with `OPENAI_API_KEY`

**Returns:** `date` object

**Raises:** `ValueError` if parsing fails or API key is missing

### Supported Date Formats

- Relative: "tomorrow", "yesterday", "today"
- Day of week: "next Monday", "this Friday", "last Tuesday"
- Relative periods: "in 3 days", "2 weeks ago", "next month"
- Specific dates: "January 1st", "March 15, 2025"

## Advanced Usage

### Reuse Client for Multiple Calls

```python
from nl_dates.llm import LLMClient

client = LLMClient()
dates = [calculate_date(d, client=client) for d in ["tomorrow", "next week"]]
```

### Custom API Key

```python
from nl_dates.llm import LLMClient

client = LLMClient(api_key="your-api-key")
result = calculate_date("tomorrow", client=client)
```

## Requirements

- Python >= 3.13
- OpenAI API key

