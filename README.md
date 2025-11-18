# nl-dates

A Python library for parsing natural language date strings into ISO datetime format.

## Installation

This project uses `uv` for dependency management. To set up the development environment:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest
```

## Usage

```python
from datetime import datetime
from nl_dates import calculate_date

# Use current datetime as reference
result = calculate_date("tomorrow")
print(result)  # Returns datetime object: datetime(2025, 11, 19, 0, 0)

# Use a specific datetime as reference
reference = datetime(2025, 1, 1, 12, 0, 0)
result = calculate_date("next week", relative_to_date=reference)
print(result)  # Returns datetime object based on reference date

# Convert to ISO format if needed
iso_string = result.isoformat()
print(iso_string)  # '2025-01-08T12:00:00'
```

## API

### `calculate_date(date_string: str, relative_to_date: datetime | None = None) -> datetime`

Convert a natural language date string to a datetime object.

**Parameters:**
- `date_string` (str): Natural language description of a date (e.g., "tomorrow", "next Tuesday")
- `relative_to_date` (datetime | None): Optional datetime to use as reference. Defaults to current datetime if not provided.

**Returns:**
- datetime: Python datetime object representing the parsed date

## Development Status

This is an early development version. The function signature and basic structure are in place.

**Implemented:**
- ✓ Project structure and development environment
- ✓ `calculate_date` function with proper type hints
- ✓ Support for optional `relative_to_date` parameter
- ✓ Returns Python datetime objects
- ✓ Modular code structure with separate parser module
- ✓ Comprehensive test suite

**TODO:**
- Natural language parsing for expressions like "tomorrow", "next Tuesday", "in 3 days", "last week", etc.

## Running Tests

```bash
uv run pytest -v
```

## Requirements

- Python >= 3.13
- uv for package management

