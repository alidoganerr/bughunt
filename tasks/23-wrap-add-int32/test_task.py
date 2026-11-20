import unittest

from solution import add_int32

MAX = 2147483647
MIN = -2147483648


class AddInt32Test(unittest.TestCase):
    def test_small_positive(self):
        self.assertEqual(add_int32(1, 2), 3)

    def test_zero(self):
        self.assertEqual(add_int32(0, 0), 0)

    def test_cancels_to_zero(self):
        self.assertEqual(add_int32(-5, 5), 0)

    def test_largest_without_overflow(self):
        self.assertEqual(add_int32(MAX - 1, 1), MAX)

    def test_positive_overflow_wraps_to_negative(self):
        self.assertEqual(add_int32(MAX, 1), MIN)

    def test_negative_result(self):
        self.assertEqual(add_int32(-1, -1), -2)

    def test_negative_overflow_wraps_to_positive(self):
        self.assertEqual(add_int32(MIN, -1), MAX)

    def test_extremes(self):
        self.assertEqual(add_int32(MAX, MAX), -2)
        self.assertEqual(add_int32(MIN, MIN), 0)

    def test_operand_out_of_range(self):
        with self.assertRaises(ValueError):
            add_int32(MAX + 1, 0)
        with self.assertRaises(ValueError):
            add_int32(0, MIN - 1)


if __name__ == "__main__":
    unittest.main()
