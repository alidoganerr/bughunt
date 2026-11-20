import unittest
from datetime import datetime, timedelta, timezone

from solution import seconds_between

PLUS3 = timezone(timedelta(hours=3))


class SecondsBetweenTest(unittest.TestCase):
    def test_both_naive(self):
        a = datetime(2024, 1, 1, 12, 0)
        b = datetime(2024, 1, 1, 12, 1)
        self.assertEqual(seconds_between(a, b), 60.0)

    def test_both_aware_utc(self):
        a = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        b = datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc)
        self.assertEqual(seconds_between(a, b), 86400.0)

    def test_aware_with_different_offsets(self):
        a = datetime(2024, 1, 1, 12, 0, tzinfo=PLUS3)
        b = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        self.assertEqual(seconds_between(a, b), 10800.0)

    def test_negative(self):
        a = datetime(2024, 1, 1, 12, 0)
        b = datetime(2024, 1, 1, 11, 0)
        self.assertEqual(seconds_between(a, b), -3600.0)

    def test_naive_start_aware_end(self):
        a = datetime(2024, 1, 1, 12, 0)
        b = datetime(2024, 1, 1, 12, 30, tzinfo=timezone.utc)
        self.assertEqual(seconds_between(a, b), 1800.0)

    def test_aware_start_naive_end(self):
        a = datetime(2024, 1, 1, 15, 0, tzinfo=PLUS3)
        b = datetime(2024, 1, 1, 13, 0)
        self.assertEqual(seconds_between(a, b), 3600.0)

    def test_returns_float(self):
        a = datetime(2024, 1, 1)
        self.assertIsInstance(seconds_between(a, a), float)


if __name__ == "__main__":
    unittest.main()
