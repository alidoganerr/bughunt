"""CSV uploads arrive here as one string."""

import csv
import io


def parse_csv(text):
    """Parse CSV text into a list of rows (lists of strings)."""
    reader = csv.reader(io.StringIO(text, newline=""))
    return [row for row in reader]
