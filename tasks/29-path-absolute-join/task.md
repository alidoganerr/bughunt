# Upload path

Write `upload_path(root, name)` in `solution.py`. `root` is a directory path using forward slashes, such as `"/srv/uploads"`. `name` is a file name chosen by a user, possibly with sub-directories (`"2024/report.txt"`). Return the path where the file should be stored: `root` and `name` joined by exactly one `/`. A single trailing `/` on `root` is not doubled.

The path must stay inside `root`. Raise `ValueError` if

- `name` is empty,
- `name` starts with `/` (it is an absolute path), or
- any `/`-separated component of `name` is exactly `..`.

Components that only start with dots, such as `..cache` or `.hidden`, are fine.

## Examples

```python
>>> upload_path("/srv/uploads", "2024/report.txt")
'/srv/uploads/2024/report.txt'
>>> try:
...     upload_path("/srv/uploads", "/etc/passwd")
... except ValueError:
...     print("rejected")
rejected
```
