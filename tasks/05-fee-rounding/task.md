# Processing fee

We charge a percentage fee on payments. Write `processing_fee(amount_cents, percent)`; both arguments are non-negative integers: a payment amount in cents and a whole-number percentage. The fee is `amount_cents * percent / 100`, rounded to a whole number of cents. Values that fall exactly halfway between two whole cents round up (for example 2.5 cents becomes 3). Return an `int`.

If either argument is negative, raise `ValueError`.

## Example

```python
>>> processing_fee(1000, 10)
100
>>> processing_fee(5, 50)
3
```
