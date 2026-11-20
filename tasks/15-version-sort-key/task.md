# Sort version strings

Write `sort_versions(versions)`. `versions` is a list of version strings of the form `major.minor.patch`, such as `"1.10.2"`. Each part is a non-negative integer, and a leading `v` is allowed (`"v1.10.2"`). Return a new list, from oldest to newest, with the original strings. Versions are compared numerically part by part. The tests do not contain two entries that mean the same version.

For example:

```python
>>> sort_versions(["1.10.0", "1.2.0", "1.9.5"])
['1.2.0', '1.9.5', '1.10.0']
```
