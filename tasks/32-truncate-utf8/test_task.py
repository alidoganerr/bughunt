import unittest

from solution import truncate_utf8


class TruncateUtf8Test(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(truncate_utf8("hello", 3), "hel")

    def test_fits_entirely(self):
        self.assertEqual(truncate_utf8("hello", 10), "hello")

    def test_exact_fit_with_multibyte(self):
        self.assertEqual(truncate_utf8("héllo", 3), "hé")

    def test_zero_budget(self):
        self.assertEqual(truncate_utf8("hello", 0), "")

    def test_empty_text(self):
        self.assertEqual(truncate_utf8("", 5), "")

    def test_cut_inside_two_byte_character(self):
        self.assertEqual(truncate_utf8("héllo", 2), "h")

    def test_cut_inside_four_byte_character(self):
        text = "a\U0001F600b"
        for budget in (2, 3, 4):
            self.assertEqual(truncate_utf8(text, budget), "a", "budget=%d" % budget)
        self.assertEqual(truncate_utf8(text, 5), "a\U0001F600")

    def test_keeps_existing_fffd(self):
        self.assertEqual(truncate_utf8("a�b", 4), "a�")

    def test_negative_budget(self):
        with self.assertRaises(ValueError):
            truncate_utf8("abc", -1)


if __name__ == "__main__":
    unittest.main()
