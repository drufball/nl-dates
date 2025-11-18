#!/usr/bin/env python3
"""Manual test script for calculate_date function."""

from datetime import date

from nl_dates import calculate_date

# Use a fixed reference date for consistent testing
reference_date = date(2025, 11, 18)

print("Testing calculate_date with OpenAI")
print(f"Reference date: {reference_date}")
print("-" * 60)

# Test 1: "tomorrow"
print("\nTest 1: 'tomorrow'")
try:
    result = calculate_date("tomorrow", relative_to_date=reference_date)
    print("Input: 'tomorrow'")
    print(f"Result: {result}")
    print("Expected: 2025-11-19")
except Exception as e:
    print(f"Error: {e}")

# Test 2: "a week from today"
print("\nTest 2: 'a week from today'")
try:
    result = calculate_date("a week from today", relative_to_date=reference_date)
    print("Input: 'a week from today'")
    print(f"Result: {result}")
    print("Expected: 2025-11-25")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "-" * 60)
print("Testing complete!")
