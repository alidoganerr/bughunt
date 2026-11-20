import unittest
from collections import defaultdict

from solution import hit_summary


class HitSummaryTest(unittest.TestCase):
    def test_present_keys(self):
        counts = {"a": 3, "b": 0}
        self.assertEqual(hit_summary(counts, ["a", "b"]), {"a": True, "b": False})

    def test_order_follows_keys(self):
        counts = {"a": 1, "b": 1}
        self.assertEqual(list(hit_summary(counts, ["b", "a"])), ["b", "a"])

    def test_empty_keys(self):
        self.assertEqual(hit_summary({"a": 1}, []), {})

    def test_missing_key_in_plain_dict(self):
        self.assertEqual(hit_summary({"a": 1}, ["z"]), {"z": False})

    def test_missing_key_in_defaultdict(self):
        counts = defaultdict(int, {"a": 2})
        self.assertEqual(hit_summary(counts, ["a", "b"]), {"a": True, "b": False})

    def test_defaultdict_is_not_modified(self):
        counts = defaultdict(int, {"a": 2})
        hit_summary(counts, ["a", "b", "c"])
        self.assertEqual(sorted(counts), ["a"])

    def test_plain_dict_is_not_modified(self):
        counts = {"a": 2}
        hit_summary(counts, ["a"])
        self.assertEqual(counts, {"a": 2})


if __name__ == "__main__":
    unittest.main()
