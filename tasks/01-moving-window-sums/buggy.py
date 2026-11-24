def moving_sums(values, k):
    """Sum of each run of k consecutive values."""
    if k < 1:
        raise ValueError("k must be at least 1")
    sums = []
    for start in range(len(values) - k):
        sums.append(sum(values[start:start + k]))
    return sums
