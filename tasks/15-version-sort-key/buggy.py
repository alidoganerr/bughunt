"""Release helpers."""


def sort_versions(versions):
    """Oldest first. "1.10.2" and "v1.10.2" are both fine."""
    keyed = [(v.lstrip("v"), v) for v in versions]
    keyed.sort()
    return [original for _, original in keyed]
