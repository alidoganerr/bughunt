import unittest

from solution import balance


class BalanceTest(unittest.TestCase):
    def test_exact_values(self):
        self.assertEqual(balance([1.5, 2.5, -1.0]), 3.0)

    def test_integers(self):
        result = balance([1, 2, 3])
        self.assertEqual(result, 6.0)
        self.assertIsInstance(result, float)

    def test_empty(self):
        self.assertEqual(balance([]), 0.0)

    def test_ten_tenths(self):
        self.assertEqual(balance([0.1] * 10), 1.0)

    def test_cancellation(self):
        self.assertEqual(balance([1e16, 1.0, -1e16]), 1.0)

    def test_many_small_entries(self):
        self.assertEqual(balance([0.01] * 100), 1.0)

    def test_running_total_drift(self):
        entries = [-0.1, 3.0, 1e16, 0.1, -1e16, 1e-05, 3.0, 0.1, 0.1]
        self.assertEqual(balance(entries), 6.20001)


if __name__ == "__main__":
    unittest.main()
