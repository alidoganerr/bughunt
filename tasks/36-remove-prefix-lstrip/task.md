# Remove a prefix

`strip_prefix(text, prefix)`: if `text` starts with `prefix`, remove it **once**. Otherwise (or if `prefix` is empty) return `text` as it is.

## Examples

```python
>>> strip_prefix("preempt", "pre")
'empt'
>>> strip_prefix("aaab", "a")
'aab'
```
