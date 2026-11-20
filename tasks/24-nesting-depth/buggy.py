"""Utilities for inspecting parsed documents."""


def nesting_depth(value):
    """How deeply lists are nested: 0 for a non-list, 1 for a flat list."""
    if not isinstance(value, list):
        return 0
    return 1 + max(nesting_depth(item) for item in value)
