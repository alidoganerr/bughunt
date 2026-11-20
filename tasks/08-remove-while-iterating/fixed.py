"""Cleaning helpers for lists of sensor readings."""


def drop_negatives(values):
    """Remove all negative readings from the list, in place."""
    values[:] = [value for value in values if value >= 0]
    return values
