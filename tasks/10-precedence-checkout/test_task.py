import unittest

from solution import can_checkout


class CanCheckoutTest(unittest.TestCase):
    def test_member_with_items(self):
        self.assertIs(can_checkout(10, True, False), True)

    def test_coupon_with_items(self):
        self.assertIs(can_checkout(10, False, True), True)

    def test_neither_member_nor_coupon(self):
        self.assertIs(can_checkout(10, False, False), False)

    def test_empty_cart_member(self):
        self.assertIs(can_checkout(0, True, False), False)

    def test_empty_cart_with_coupon(self):
        self.assertIs(can_checkout(0, False, True), False)

    def test_blocked_member(self):
        self.assertIs(can_checkout(10, True, False, blocked=True), False)

    def test_blocked_with_coupon(self):
        self.assertIs(can_checkout(10, False, True, blocked=True), False)


if __name__ == "__main__":
    unittest.main()
