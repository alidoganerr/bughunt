"""Text measurement for a label printer."""

import unicodedata


def visible_length(text):
    """Number of base characters in text; accents are not counted."""
    composed = unicodedata.normalize("NFC", text)
    return len(composed)
