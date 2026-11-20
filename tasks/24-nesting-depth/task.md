# Nesting depth

`nesting_depth(value)` returns how deeply `list` objects are nested inside `value`.

- A value that is not a `list` has depth `0`. Tuples, strings and dicts are not lists.
- A list has depth `1` plus the greatest depth among its items. An empty list has depth `1`.

## Examples

```python
>>> nesting_depth(5)
0
>>> nesting_depth([1, [2, [3]]])
3
>>> nesting_depth([1, []])
2
```
