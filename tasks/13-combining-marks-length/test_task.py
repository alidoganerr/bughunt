import unittest

from solution import visible_length


class VisibleLengthTest(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(visible_length("hello"), 5)

    def test_empty(self):
        self.assertEqual(visible_length(""), 0)

    def test_precomposed(self):
        self.assertEqual(visible_length("caf\u00e9"), 4)

    def test_decomposed_with_composed_form(self):
        self.assertEqual(visible_length("cafe\u0301"), 4)

    def test_cjk_and_emoji(self):
        self.assertEqual(visible_length("\u65e5\u672c\U0001F44D"), 3)

    def test_mark_without_precomposed_letter(self):
        self.assertEqual(visible_length("q\u0301"), 1)

    def test_stacked_marks(self):
        self.assertEqual(visible_length("a\u0300\u0323"), 1)

    def test_mark_after_each_letter(self):
        self.assertEqual(visible_length("x\u0301y\u0301z\u0301"), 3)


if __name__ == "__main__":
    unittest.main()
