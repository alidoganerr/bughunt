"""Text measurement for a label printer."""

import unicodedata


def visible_length(text):
    """Number of base characters in text; accents are not counted."""
    return sum(1 for ch in text if not unicodedata.combining(ch))
