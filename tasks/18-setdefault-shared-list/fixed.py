"""Collection helpers."""


def group_by(items, key):
    """Group items into {key(item): [items...]}, keeping input order."""
    groups = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups
