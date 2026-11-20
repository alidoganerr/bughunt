"""Threshold checks for a monitoring script."""


def build_checks(limits):
    """Return {name: check}; check(value) is True when value <= that limit."""
    checks = {}
    for name, limit in limits.items():
        if limit < 0:
            raise ValueError("limit for %s is negative" % name)
        checks[name] = lambda value: value <= limit
    return checks
