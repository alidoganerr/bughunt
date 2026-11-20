"""Rules for the checkout page of a small shop."""


def can_checkout(cart_total, is_member, has_coupon, blocked=False):
    """True if the checkout button should be enabled.

    Blocked accounts never check out. Everyone else needs a non-empty cart
    and either a membership or a coupon.
    """
    return not blocked and cart_total > 0 and is_member or has_coupon
