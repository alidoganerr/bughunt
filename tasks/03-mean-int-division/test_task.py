import unittest

from solution import mean


class MeanTest(unittest.TestCase):
    def test_exact_mean(self):
        self.assertEqual(mean([2, 4, 6]), 4)

    def test_fractional_mean(self):
        self.assertEqual(mean([1, 2]), 1.5)

    def test_negative_mean(self):
        self.assertEqual(mean([-3, 0]), -1.5)

    def test_single_value(self):
        self.assertEqual(mean([7]), 7)

    def test_floats(self):
        self.assertEqual(mean([0.5, 1.5]), 1.0)

    def test_tuple(self):
        self.assertEqual(mean((1, 1, 2)), 4 / 3)

    def test_returns_float(self):
        self.assertIsInstance(mean([2, 4]), float)

    def test_empty(self):
        with self.assertRaises(ValueError):
            mean([])


if __name__ == "__main__":
    unittest.main()
