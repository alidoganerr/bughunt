# Parse JSON or fall back

Write `load_or_default(text, default=None)`. `text` is supposed to be a JSON string.

- If `text` is valid JSON, return the parsed value.
- If `text` is a `str` that is not valid JSON (including the empty string), return `default`.
- If `text` is not a `str` at all (for example `None` or an `int`), that is a programming error: let the `TypeError` that `json.loads` raises propagate. Do not return `default`.

## Examples

```python
>>> load_or_default('{"a": 1}')
{'a': 1}
>>> load_or_default("{oops", default={})
{}
>>> try:
...     load_or_default(None, default={})
... except TypeError:
...     print("TypeError")
TypeError
```
