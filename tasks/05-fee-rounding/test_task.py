import unittest

from solution import processing_fee


class ProcessingFeeTest(unittest.TestCase):
    def test_whole_cents(self):
        self.assertEqual(processing_fee(1000, 10), 100)

    def test_rounds_down_below_half(self):
        self.assertEqual(processing_fee(149, 1), 1)

    def test_rounds_up_above_half(self):
        self.assertEqual(processing_fee(151, 1), 2)

    def test_half_rounds_up_from_odd(self):
        self.assertEqual(processing_fee(150, 1), 2)

    def test_half_rounds_up_from_even(self):
        self.assertEqual(processing_fee(5, 50), 3)
        self.assertEqual(processing_fee(250, 1), 3)
        self.assertEqual(processing_fee(25, 10), 3)

    def test_zero(self):
        self.assertEqual(processing_fee(0, 15), 0)

    def test_returns_int(self):
        self.assertIsInstance(processing_fee(5, 50), int)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            processing_fee(-1, 10)
        with self.assertRaises(ValueError):
            processing_fee(100, -1)


if __name__ == "__main__":
    unittest.main()
