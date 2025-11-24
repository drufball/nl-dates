#!/usr/bin/env python3
"""Manual test script for extract_date function."""

from datetime import date, timedelta

from nl_dates import extract_date

# Use today as reference date
reference_date = date.today()

print("Testing extract_date with OpenAI")
print(f"Reference date: {reference_date}")
print("-" * 60)

# Test 1: Task with natural language date
print("\nTest 1: Task with date context")
try:
    task = "Submit report tomorrow"
    cleaned_task, extracted_date = extract_date(task, relative_to_date=reference_date)
    print(f"Input: '{task}'")
    print(f"Cleaned task: '{cleaned_task}'")
    print(f"Extracted date: {extracted_date}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Task without date
print("\nTest 2: Task without date context")
try:
    task = "Fix the authentication bug"
    cleaned_task, extracted_date = extract_date(task, relative_to_date=reference_date)
    print(f"Input: '{task}'")
    print(f"Cleaned task: '{cleaned_task}'")
    print(f"Extracted date: {extracted_date}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Task with relative date
print("\nTest 3: Task with relative date")
try:
    task = "Deploy in 3 days"
    cleaned_task, extracted_date = extract_date(task, relative_to_date=reference_date)
    print(f"Input: '{task}'")
    print(f"Cleaned task: '{cleaned_task}'")
    print(f"Extracted date: {extracted_date}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "-" * 60)
print("Testing complete!")
