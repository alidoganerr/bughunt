"""Timestamps from different systems."""

from datetime import timezone


def _as_utc(moment):
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def seconds_between(start, end):
    """Seconds from start to end (negative if end is earlier).

    Naive datetimes are treated as UTC.
    """
    return (_as_utc(end) - _as_utc(start)).total_seconds()
