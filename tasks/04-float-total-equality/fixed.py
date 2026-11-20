"""Invoice checks."""


def totals_match(line_items, expected_total):
    """Do the line items add up to the total printed on the invoice?"""
    total = 0.0
    for unit_price, quantity in line_items:
        total += unit_price * quantity
    return abs(total - expected_total) < 0.005
