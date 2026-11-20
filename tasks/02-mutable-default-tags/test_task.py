import unittest

from solution import add_tag


class AddTagTest(unittest.TestCase):
    def test_adds_to_given_list(self):
        self.assertEqual(add_tag("b", ["a"]), ["a", "b"])

    def test_normalises(self):
        self.assertEqual(add_tag("  Python ", ["x"]), ["x", "python"])

    def test_no_duplicates(self):
        self.assertEqual(add_tag("A", ["a", "b"]), ["a", "b"])

    def test_empty_tag(self):
        with self.assertRaises(ValueError):
            add_tag("   ", ["a"])

    def test_returns_new_list(self):
        original = ["a"]
        result = add_tag("b", original)
        self.assertIsNot(result, original)

    def test_given_list_not_modified(self):
        original = ["a"]
        add_tag("b", original)
        self.assertEqual(original, ["a"])

    def test_default_calls_are_independent(self):
        self.assertEqual(add_tag("first"), ["first"])
        self.assertEqual(add_tag("second"), ["second"])

    def test_none_means_empty(self):
        self.assertEqual(add_tag("z", None), ["z"])


if __name__ == "__main__":
    unittest.main()
