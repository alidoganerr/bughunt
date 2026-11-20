# Parse a header line

Write `parse_header(line)` for lines like `Name: value`. It returns a tuple `(name, value)`.

- `name` is the text before the **first** colon, with surrounding whitespace removed and converted to lower case.
- `value` is everything after the first colon, with surrounding whitespace removed. It may itself contain colons.
- If `line` contains no colon, raise `ValueError`.

Example:

```python
>>> parse_header("Host: example.com:8080")
('host', 'example.com:8080')
```
