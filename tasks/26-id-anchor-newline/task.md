# Validate an identifier

Write `is_valid_id(text)` in `solution.py`. Return `True` if `text` is exactly two uppercase ASCII letters (`A` to `Z`), a hyphen, and exactly four ASCII digits (`0` to `9`), such as `"AB-1234"`. Return `False` for anything else. Nothing else is allowed around it. Leading/trailing spaces or a trailing newline make it invalid.

## Example

```python
>>> is_valid_id("AB-1234")
True
>>> is_valid_id("AB-1234\n")
False
```
