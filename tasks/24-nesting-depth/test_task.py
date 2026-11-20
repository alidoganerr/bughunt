import unittest

from solution import nesting_depth


class NestingDepthTest(unittest.TestCase):
    def test_scalar(self):
        self.assertEqual(nesting_depth(5), 0)

    def test_string_is_not_a_list(self):
        self.assertEqual(nesting_depth("abc"), 0)

    def test_flat_list(self):
        self.assertEqual(nesting_depth([1, 2, 3]), 1)

    def test_nested(self):
        self.assertEqual(nesting_depth([1, [2, [3]]]), 3)

    def test_uneven_branches(self):
        self.assertEqual(nesting_depth([[1], [[2]], 3]), 3)

    def test_tuple_is_not_a_list(self):
        self.assertEqual(nesting_depth([(1, [2])]), 1)

    def test_empty_list(self):
        self.assertEqual(nesting_depth([]), 1)

    def test_empty_list_inside(self):
        self.assertEqual(nesting_depth([1, []]), 2)

    def test_only_empty_lists(self):
        self.assertEqual(nesting_depth([[], [[]]]), 3)


if __name__ == "__main__":
    unittest.main()
