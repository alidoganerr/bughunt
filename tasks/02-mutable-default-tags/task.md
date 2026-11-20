# Add a tag

`add_tag(tag, tags=None)` returns a new list made of the items of `tags` (an empty list when `tags` is omitted or `None`) followed by the normalised `tag`.

- The tag is normalised by stripping surrounding whitespace and lower-casing it.
- If the normalised tag is empty, raise `ValueError`.
- If the normalised tag is already in `tags`, it is not added a second time.
- The list passed in as `tags` is never modified.
- Calls that omit `tags` are independent of each other.

## Examples

```python
>>> add_tag("Python")
['python']
>>> add_tag("Testing")
['testing']
>>> add_tag(" bugs ", ["python"])
['python', 'bugs']
```
