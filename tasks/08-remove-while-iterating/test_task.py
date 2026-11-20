import unittest

from solution import drop_negatives


class DropNegativesTest(unittest.TestCase):
    def test_no_negatives(self):
        self.assertEqual(drop_negatives([1, 2, 3]), [1, 2, 3])

    def test_separated_negatives(self):
        self.assertEqual(drop_negatives([-1, 2, -3, 4]), [2, 4])

    def test_adjacent_negatives(self):
        self.assertEqual(drop_negatives([1, -1, -2, 3]), [1, 3])

    def test_all_negative(self):
        self.assertEqual(drop_negatives([-1, -2, -3]), [])

    def test_zero_is_kept(self):
        self.assertEqual(drop_negatives([0, -0.0, -1]), [0, -0.0])

    def test_empty(self):
        self.assertEqual(drop_negatives([]), [])

    def test_same_list_object(self):
        data = [-1, -2, 5]
        result = drop_negatives(data)
        self.assertIs(result, data)
        self.assertEqual(data, [5])


if __name__ == "__main__":
    unittest.main()
