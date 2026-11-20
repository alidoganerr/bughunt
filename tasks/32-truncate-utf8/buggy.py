"""Fitting text into fixed-size database columns."""


def truncate_utf8(text, max_bytes):
    """Longest prefix of text whose UTF-8 form fits in max_bytes bytes."""
    if max_bytes < 0:
        raise ValueError("max_bytes must not be negative")
    data = text.encode("utf-8")[:max_bytes]
    return data.decode("utf-8", errors="replace")
