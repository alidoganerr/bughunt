# Drop negative numbers

`drop_negatives(values)` removes every negative number from the list `values` **in place** and returns that same list object. Order of what is left is kept. Zero stays (it isn't negative).

```python
>>> data = [1, -1, -2, 3]
>>> drop_negatives(data)
[1, 3]
>>> data
[1, 3]
```
