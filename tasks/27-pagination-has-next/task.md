# One page of results

Write `paginate(items, page, per_page)`. Pages start at 1. It returns a dict with these keys:

- `"items"`: the slice of `items` that belongs to `page` (an empty list if the page is past the end).
- `"page"`: the `page` argument.
- `"pages"`: the number of pages needed for all items, which is `0` for an empty list.
- `"has_next"`: `True` if at least one item comes after this page, otherwise `False`.

If `page < 1` or `per_page < 1`, raise `ValueError`.

## Example

```python
>>> paginate([1, 2, 3, 4], 2, 2)
{'items': [3, 4], 'page': 2, 'pages': 2, 'has_next': False}
```
