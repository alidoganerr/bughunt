"""Collection helpers."""


def group_by(items, key):
    """Group items into {key(item): [items...]}, keeping input order."""
    groups = {}
    empty = []
    for item in items:
        groups.setdefault(key(item), empty).append(item)
    return groups
