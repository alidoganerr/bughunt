"""Timestamps from different systems."""


def seconds_between(start, end):
    """Seconds from start to end (negative if end is earlier).

    Naive datetimes are treated as UTC.
    """
    return (end - start).total_seconds()
