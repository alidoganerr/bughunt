import unittest
from datetime import date

from solution import add_months


class AddMonthsTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(add_months(date(2024, 1, 15), 1), date(2024, 2, 15))

    def test_clamps_to_end_of_february(self):
        self.assertEqual(add_months(date(2023, 1, 31), 1), date(2023, 2, 28))

    def test_clamps_to_leap_day(self):
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))

    def test_thirty_day_month(self):
        self.assertEqual(add_months(date(2024, 3, 31), 1), date(2024, 4, 30))

    def test_crosses_year_end(self):
        self.assertEqual(add_months(date(2023, 12, 31), 2), date(2024, 2, 29))

    def test_zero(self):
        self.assertEqual(add_months(date(2024, 6, 5), 0), date(2024, 6, 5))

    def test_many_years(self):
        self.assertEqual(add_months(date(2023, 10, 9), 25), date(2025, 11, 9))

    def test_negative_clamps(self):
        self.assertEqual(add_months(date(2024, 3, 31), -1), date(2024, 2, 29))

    def test_lands_in_december(self):
        self.assertEqual(add_months(date(2023, 11, 30), 1), date(2023, 12, 30))

    def test_negative_into_december(self):
        self.assertEqual(add_months(date(2024, 1, 15), -1), date(2023, 12, 15))

    def test_twelve_months_from_december(self):
        self.assertEqual(add_months(date(2023, 12, 5), 12), date(2024, 12, 5))


if __name__ == "__main__":
    unittest.main()
