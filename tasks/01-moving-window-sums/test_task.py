import unittest

from solution import moving_sums


class MovingSumsTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(moving_sums([1, 2, 3, 4, 5], 2), [3, 5, 7, 9])

    def test_window_of_one(self):
        self.assertEqual(moving_sums([1, 2, 3], 1), [1, 2, 3])

    def test_window_equals_length(self):
        self.assertEqual(moving_sums([4, 4], 2), [8])

    def test_window_larger_than_input(self):
        self.assertEqual(moving_sums([1, 2], 5), [])

    def test_empty_input(self):
        self.assertEqual(moving_sums([], 3), [])

    def test_floats(self):
        self.assertEqual(moving_sums([0.5, 0.25, 0.25], 3), [1.0])

    def test_invalid_window(self):
        with self.assertRaises(ValueError):
            moving_sums([1, 2, 3], 0)

    def test_input_not_modified(self):
        data = [3, 1, 2]
        moving_sums(data, 2)
        self.assertEqual(data, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
