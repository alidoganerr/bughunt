# Order tasks by priority

`order_tasks(tasks)`: `tasks` is a list of dicts, each with a `"name"` and an integer `"priority"`. Return a new list with the same dicts ordered from the highest priority to the lowest. Tasks with the same priority keep the order they had in `tasks`. The input list is not modified.

## Example

```python
>>> tasks = [
...     {"name": "a", "priority": 1},
...     {"name": "b", "priority": 2},
...     {"name": "c", "priority": 2},
... ]
>>> [t["name"] for t in order_tasks(tasks)]
['b', 'c', 'a']
```
