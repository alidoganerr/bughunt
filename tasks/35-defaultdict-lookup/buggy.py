"""Report helpers for hit counters."""


def hit_summary(counts, keys):
    """Return {key: True/False}: which of keys have a positive count.

    `counts` is a dict or a defaultdict(int); it must not be modified.
    """
    return {key: counts[key] > 0 for key in keys}
