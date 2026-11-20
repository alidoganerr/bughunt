import unittest

from solution import bold_texts


class BoldTextsTest(unittest.TestCase):
    def test_single(self):
        self.assertEqual(bold_texts("a <b>x</b> b"), ["x"])

    def test_none(self):
        self.assertEqual(bold_texts("plain text"), [])

    def test_empty_element(self):
        self.assertEqual(bold_texts("<b></b>"), [""])

    def test_one_per_line(self):
        self.assertEqual(bold_texts("<b>x</b>\n<b>y</b>"), ["x", "y"])

    def test_two_on_one_line(self):
        self.assertEqual(bold_texts("<b>one</b> and <b>two</b>"), ["one", "two"])

    def test_three_with_other_markup_between(self):
        html = "<b>a</b><i>m</i><b>b</b> text <b>c</b>"
        self.assertEqual(bold_texts(html), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
