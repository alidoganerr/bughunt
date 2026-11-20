"""Normalisation helpers."""


def scale_to_unit(values):
    """Divide each value by the maximum so that the largest becomes 1.0."""
    peak = max(values, default=0)
    if peak == 0:
        return [0.0 for _ in values]
    return [v / peak for v in values]
