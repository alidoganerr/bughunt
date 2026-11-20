"""Validation for ids typed into a form field."""

import re

ID_PATTERN = re.compile(r"^[A-Z]{2}-[0-9]{4}$")


def is_valid_id(text):
    """True for ids shaped like "AB-1234"."""
    return ID_PATTERN.match(text) is not None
