# Add months to a date

Write `add_months(d, months)`. `d` is a `datetime.date`, `months` any integer (negative is fine). Return the date that is `months` calendar months away from `d`, with the same day of the month. If that day does not exist in the target month, use the last day of the target month instead (so January 31 plus one month is the last day of February).

## Examples

```python
>>> from datetime import date
>>> add_months(date(2024, 1, 31), 1)
datetime.date(2024, 2, 29)
>>> add_months(date(2023, 11, 30), 1)
datetime.date(2023, 12, 30)
```
