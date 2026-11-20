# Truncate to a byte budget

We store text in columns with a byte limit. Write `truncate_utf8(text, max_bytes)` that returns the longest prefix of `text` whose UTF-8 encoding is at most `max_bytes` bytes long. A character is never cut in the middle: if it does not fit completely, it is left out, along with everything after it. If the whole text fits, return it unchanged. The result is always a valid `str` and never contains replacement characters that were not already in `text`.

If `max_bytes` is negative, raise `ValueError`.

## Example

```python
>>> truncate_utf8("hello", 3)
'hel'
>>> truncate_utf8("héllo", 2)
'h'
```
