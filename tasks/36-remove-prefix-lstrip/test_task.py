import unittest

from solution import strip_prefix


class StripPrefixTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(strip_prefix("v1.2", "v"), "1.2")

    def test_no_match(self):
        self.assertEqual(strip_prefix("hello", "x"), "hello")

    def test_empty_prefix(self):
        self.assertEqual(strip_prefix("hello", ""), "hello")

    def test_whole_text_is_the_prefix(self):
        self.assertEqual(strip_prefix("abc", "abc"), "")

    def test_prefix_letters_repeat_in_text(self):
        self.assertEqual(strip_prefix("preempt", "pre"), "empt")

    def test_only_one_occurrence_is_removed(self):
        self.assertEqual(strip_prefix("aaab", "a"), "aab")

    def test_prefix_not_at_start(self):
        self.assertEqual(strip_prefix("xxpre", "pre"), "xxpre")


if __name__ == "__main__":
    unittest.main()
