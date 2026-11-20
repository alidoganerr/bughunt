# Scale to the unit interval

Implement `scale_to_unit(values)`. `values` can be any iterable of non-negative numbers: a list, a tuple or a generator that can be consumed only once. Return a list of floats in which every value is divided by the largest value, so the largest becomes `1.0`. If the iterable is empty, return `[]`. If every value is zero, return a list of `0.0` of the same length.

## Examples

```python
>>> scale_to_unit([1, 2, 4])
[0.25, 0.5, 1.0]
>>> scale_to_unit(v for v in [1, 2, 4])
[0.25, 0.5, 1.0]
```
