import unittest

from solution import is_valid_id


class IsValidIdTest(unittest.TestCase):
    def test_valid(self):
        self.assertIs(is_valid_id("AB-1234"), True)

    def test_lowercase_letters(self):
        self.assertIs(is_valid_id("ab-1234"), False)

    def test_too_many_digits(self):
        self.assertIs(is_valid_id("AB-12345"), False)

    def test_too_few_digits(self):
        self.assertIs(is_valid_id("AB-123"), False)

    def test_extra_prefix(self):
        self.assertIs(is_valid_id("XAB-1234"), False)

    def test_leading_space(self):
        self.assertIs(is_valid_id(" AB-1234"), False)

    def test_trailing_space(self):
        self.assertIs(is_valid_id("AB-1234 "), False)

    def test_non_ascii_digits(self):
        self.assertIs(is_valid_id("AB-١٢٣٤"), False)

    def test_empty(self):
        self.assertIs(is_valid_id(""), False)

    def test_trailing_newline(self):
        self.assertIs(is_valid_id("AB-1234\n"), False)


if __name__ == "__main__":
    unittest.main()
