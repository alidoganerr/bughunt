# Add two int32 values

Write `add_int32(a, b)`, where `a` and `b` are Python integers in the signed 32-bit range `-2147483648 .. 2147483647`. Return their sum as a signed 32-bit integer using two's complement wraparound, so the result is always in the same range. For example `2147483647 + 1` wraps to `-2147483648`.

If `a` or `b` is outside the 32-bit range, raise `ValueError`.

## Example

```python
>>> add_int32(2147483647, 1)
-2147483648
>>> add_int32(-1, -1)
-2
```
