import calendar
from datetime import date


def add_months(d, months):
    """Return d moved by `months` calendar months (may be negative)."""
    total = d.year * 12 + (d.month - 1) + months
    year, month_index = divmod(total, 12)
    month = month_index + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)
