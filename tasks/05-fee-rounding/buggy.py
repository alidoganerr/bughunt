"""Payment fee calculation."""


def processing_fee(amount_cents, percent):
    """Fee in whole cents for a payment of amount_cents."""
    if amount_cents < 0 or percent < 0:
        raise ValueError("amount and percent must not be negative")
    fee = amount_cents * percent / 100
    return round(fee)
