"""Bookkeeping helpers."""

import math


def balance(entries):
    """Sum of ledger entries, as a float."""
    return math.fsum(entries)
