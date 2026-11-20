"""Bookkeeping helpers."""


def balance(entries):
    """Sum of ledger entries, as a float."""
    total = 0.0
    for amount in entries:
        total += amount
    return total
