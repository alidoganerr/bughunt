# Read a setting

Write `get_setting(config, key, default=None)` for a plain dict `config`. If `key` is a key of `config`, return the stored value, whatever it is: `0`, `False`, an empty string, an empty list and `None` are all valid stored values and must be returned as they are. If `key` is not in `config`, return `default`.

Example:

```python
>>> get_setting({"retries": 0}, "retries", 3)
0
>>> get_setting({}, "retries", 3)
3
```
