# Settings store

A class this time: `Settings`, in `solution.py`.

- `Settings(values=None)` starts with a copy of the dict `values` (empty if `None`). Changing the dict that was passed in later does not affect the store.
- `get(key)` returns the value currently stored under `key`. If the key is missing it raises `KeyError`.
- `set(key, value)` stores `value` under `key`. Every later `get(key)` returns the new value.
- Separate `Settings` objects never see each other's values.

## Example

```python
>>> s = Settings({"mode": "fast"})
>>> s.get("mode")
'fast'
>>> s.set("mode", "safe")
>>> s.get("mode")
'safe'
```
