"""Release helpers."""


def sort_versions(versions):
    """Oldest first. "1.10.2" and "v1.10.2" are both fine."""

    def key(version):
        return tuple(int(part) for part in version.lstrip("v").split("."))

    return sorted(versions, key=key)
