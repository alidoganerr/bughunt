# Validate rows

`check_rows(rows)` validates a list of dicts (rows from an import). Check **every** row and return a list of problem strings in row order. Rows are numbered from 1. For each row, in this order:

1. If `row.get("name")` is missing or empty, add `"row N: missing name"`.
2. If `row.get("qty", 0)` is negative, add `"row N: negative qty"`.

A single row can produce both messages (name first). If there are no problems, return an empty list.

## Example

```python
>>> rows = [{"name": ""}, {"name": "b", "qty": -2}]
>>> check_rows(rows)
['row 1: missing name', 'row 2: negative qty']
```
