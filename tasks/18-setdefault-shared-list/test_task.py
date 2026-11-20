import unittest

from solution import group_by


class GroupByTest(unittest.TestCase):
    def test_single_group(self):
        self.assertEqual(group_by(["a", "ab", "ac"], lambda s: s[0]), {"a": ["a", "ab", "ac"]})

    def test_two_groups(self):
        result = group_by(["apple", "avocado", "banana"], lambda s: s[0])
        self.assertEqual(result, {"a": ["apple", "avocado"], "b": ["banana"]})

    def test_numbers(self):
        self.assertEqual(
            group_by([1, 2, 3, 4, 5], lambda n: n % 2),
            {1: [1, 3, 5], 0: [2, 4]},
        )

    def test_order_of_groups(self):
        result = group_by([3, 1, 2, 4], lambda n: n % 2)
        self.assertEqual(list(result), [1, 0])

    def test_empty(self):
        self.assertEqual(group_by([], len), {})

    def test_groups_are_separate_lists(self):
        result = group_by(["x", "yy"], len)
        result[1].append("new")
        self.assertEqual(result[2], ["yy"])


if __name__ == "__main__":
    unittest.main()
