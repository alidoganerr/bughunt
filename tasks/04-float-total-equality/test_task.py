import unittest

from solution import totals_match


class TotalsMatchTest(unittest.TestCase):
    def test_exact_binary_values(self):
        self.assertIs(totals_match([(2.5, 2)], 5.0), True)

    def test_point_one_plus_point_two(self):
        self.assertIs(totals_match([(0.1, 1), (0.2, 1)], 0.3), True)

    def test_accumulated_rounding_error(self):
        self.assertIs(totals_match([(0.1, 10)], 1.0), True)

    def test_clearly_different(self):
        self.assertIs(totals_match([(10.0, 1)], 10.01), False)

    def test_small_difference_is_accepted(self):
        self.assertIs(totals_match([(10.0, 1)], 10.004), True)

    def test_empty_invoice(self):
        self.assertIs(totals_match([], 0.0), True)

    def test_empty_invoice_nonzero_total(self):
        self.assertIs(totals_match([], 1.0), False)


    def test_rounding_would_hide_difference(self):
        self.assertIs(totals_match([(1.004, 1)], 1.006), True)

    def test_just_over_half_cent(self):
        self.assertIs(totals_match([(1.0, 1)], 1.006), False)


if __name__ == "__main__":
    unittest.main()
