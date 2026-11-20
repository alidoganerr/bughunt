# Role lookup

Write `has_role(roles, wanted)`. `roles` is a list of role name strings, usually parsed out of a config value. Return `True` if `wanted` is equal to any item of `roles`, case-sensitive, and `False` otherwise.

## Example

```python
>>> roles = "admin,editor".split(",")
>>> has_role(roles, "admin")
True
>>> has_role(roles, "viewer")
False
```
