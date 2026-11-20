# Ledger balance

`balance(entries)` adds up a list of ledger entries (credits positive, debits negative) and returns a `float`. The result must be the exact mathematical sum of the values, rounded once to the nearest float, so tiny errors do not build up when many entries are added. For example, ten entries of `0.1` must give exactly `1.0`. An empty list gives `0.0`.

## Examples

```python
>>> balance([0.1] * 10)
1.0
>>> balance([1e16, 1.0, -1e16])
1.0
```
