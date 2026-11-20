# Seconds between two timestamps

Write `seconds_between(start, end)` in `solution.py`. Both arguments are `datetime.datetime` objects; return the seconds from `start` to `end` as a `float`. The result is negative if `end` is earlier than `start`.

- A datetime with a timezone (an aware datetime) is compared by the instant it represents, so `12:00+03:00` is three hours earlier than `12:00+00:00`.
- A datetime without a timezone (a naive datetime) is treated as UTC.
- The two arguments may be any mix of naive and aware datetimes.

## Example

```python
>>> from datetime import datetime, timezone
>>> naive = datetime(2024, 1, 1, 12, 0)
>>> aware = datetime(2024, 1, 1, 12, 30, tzinfo=timezone.utc)
>>> seconds_between(naive, aware)
1800.0
```
