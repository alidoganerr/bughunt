# Checkout button

`can_checkout(cart_total, is_member, has_coupon, blocked=False)` decides whether the checkout button is enabled. Rules:

- A blocked account can never check out.
- Otherwise the cart total must be greater than zero, and in addition the customer must be a member or hold a coupon.

Return a real `bool`.

## Example

```python
>>> can_checkout(0, False, True)
False
>>> can_checkout(25.0, True, False, blocked=True)
False
```
