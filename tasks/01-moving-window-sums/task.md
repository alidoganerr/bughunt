# Moving window sums

`moving_sums(values, k)` takes a list of numbers and a window size `k`, and returns the sum of every run of `k` consecutive values, in order. For a list of length `n` and `1 <= k <= n` the result has `n - k + 1` items. If `k` is larger than `len(values)` the result is an empty list. `values` must not be modified.

If `k < 1`, raise `ValueError`.

## Example

```python
>>> moving_sums([1, 2, 3, 4, 5], 2)
[3, 5, 7, 9]
>>> moving_sums([4, 4], 2)
[8]
```
