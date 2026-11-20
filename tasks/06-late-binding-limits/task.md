# Limit checks

`build_checks(limits)` gets a dict that maps a name to the largest value allowed for that name. It returns a dict with the same keys. Each value is a function `check(value)` that returns `True` when `value <= limit` for the limit belonging to that key, and `False` otherwise.

If any limit is negative, raise `ValueError` before returning anything.

## Example

```python
>>> checks = build_checks({"cpu": 80, "memory": 10})
>>> checks["cpu"](50)
True
>>> checks["memory"](50)
False
```
