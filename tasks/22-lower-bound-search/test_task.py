import unittest

from solution import lower_bound


class LowerBoundTest(unittest.TestCase):
    def test_target_present(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 5), 2)

    def test_target_between_items(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 4), 2)

    def test_target_below_all(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 0), 0)

    def test_target_equals_first(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 1), 0)

    def test_target_equals_last(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 7), 3)

    def test_target_above_all(self):
        self.assertEqual(lower_bound([1, 3, 5, 7], 8), 4)

    def test_duplicates_return_first(self):
        self.assertEqual(lower_bound([1, 3, 3, 3, 7], 3), 1)

    def test_single_item(self):
        self.assertEqual(lower_bound([5], 5), 0)
        self.assertEqual(lower_bound([5], 6), 1)

    def test_empty(self):
        self.assertEqual(lower_bound([], 1), 0)

    def test_every_position_in_a_longer_list(self):
        data = [2, 4, 4, 6, 8, 8, 8, 10]
        for target in range(0, 13):
            expected = sum(1 for v in data if v < target)
            self.assertEqual(lower_bound(data, target), expected, "target=%d" % target)


if __name__ == "__main__":
    unittest.main()
