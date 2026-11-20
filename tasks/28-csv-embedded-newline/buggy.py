"""CSV uploads arrive here as one string."""

import csv


def parse_csv(text):
    """Parse CSV text into a list of rows (lists of strings)."""
    reader = csv.reader(text.splitlines())
    return [row for row in reader]
