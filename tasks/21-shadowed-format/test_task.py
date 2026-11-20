import unittest

from solution import render


class RenderTest(unittest.TestCase):
    def test_short_is_the_default(self):
        self.assertEqual(render([1, 2, 3]), "3 values")

    def test_short_explicit(self):
        self.assertEqual(render([], format="short"), "0 values")

    def test_one_values(self):
        self.assertEqual(render([5], format="short"), "1 values")

    def test_unknown_format(self):
        with self.assertRaises(ValueError):
            render([1], format="medium")

    def test_long_empty(self):
        self.assertEqual(render([], format="long"), "")

    def test_long(self):
        self.assertEqual(render([1, 2.5], format="long"), "1.0, 2.5")

    def test_long_rounds_to_one_digit(self):
        self.assertEqual(render([0.04, 3.26], format="long"), "0.0, 3.3")


if __name__ == "__main__":
    unittest.main()
