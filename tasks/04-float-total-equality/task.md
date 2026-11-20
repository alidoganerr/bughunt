# Invoice total check

Write `totals_match(line_items, expected_total)`. `line_items` is a list of `(unit_price, quantity)` pairs and `expected_total` is the total stated on the invoice. Prices are floats in currency units (dollars, say). Return `True` if the computed total is within half a cent of the expected total, that is if `abs(total - expected_total) < 0.005`, and `False` otherwise. An empty list has a total of `0.0`.

Tests never use differences of exactly half a cent.

## Example

```python
>>> totals_match([(0.1, 1), (0.2, 1)], 0.3)
True
>>> totals_match([(10.0, 1)], 10.01)
False
```
