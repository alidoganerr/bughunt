# Group items by key

`group_by(items, key)` takes a list and a key function and returns a dict that maps each distinct `key(item)` to the list of items that produced it. Within a group the items keep their input order. The groups appear in the dict in order of first appearance. Every group must be a separate list.

## Example

```python
>>> group_by(["apple", "avocado", "banana"], lambda s: s[0])
{'a': ['apple', 'avocado'], 'b': ['banana']}
```
