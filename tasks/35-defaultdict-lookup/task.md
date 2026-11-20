# Which counters have hits

Write `hit_summary(counts, keys)` in `solution.py`. `counts` is either a plain `dict` or a `collections.defaultdict(int)` mapping names to non-negative integer counts. `keys` is a list of names. Return a dict that maps each name in `keys` to `True` if `counts` holds a count greater than zero for it, and to `False` otherwise (including when the name is not in `counts` at all). The result follows the order of `keys`.

`counts` must not be modified: after the call it has exactly the keys it had before, whatever its type.

## Example

```python
>>> from collections import defaultdict
>>> counts = defaultdict(int, {"a": 2})
>>> hit_summary(counts, ["a", "b"])
{'a': True, 'b': False}
>>> sorted(counts)
['a']
```
