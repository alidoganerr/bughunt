"""String helpers for a path and name cleaner."""


def strip_prefix(text, prefix):
    """Remove prefix from the start of text, once, if it is there.

    Text that does not start with prefix is returned unchanged.
    """
    return text.lstrip(prefix)
