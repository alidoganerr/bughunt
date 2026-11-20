# Lower bound in a sorted list

Implement `lower_bound(values, target)`. `values` is a list of numbers sorted in ascending order (duplicates allowed). Return the smallest index `i` such that `values[i] >= target`. If every item is smaller than `target`, return `len(values)`. For an empty list return `0`. Do not modify `values`.

## Examples

```python
>>> lower_bound([1, 3, 3, 7], 3)
1
>>> lower_bound([1, 3, 3, 7], 8)
4
```
