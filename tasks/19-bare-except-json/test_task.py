import unittest

from solution import load_or_default


class LoadOrDefaultTest(unittest.TestCase):
    def test_valid_object(self):
        self.assertEqual(load_or_default('{"a": [1, 2]}'), {"a": [1, 2]})

    def test_valid_scalar(self):
        self.assertEqual(load_or_default("3.5", default=0), 3.5)

    def test_valid_null_is_not_the_default(self):
        self.assertIsNone(load_or_default("null", default="fallback"))

    def test_invalid_text(self):
        self.assertEqual(load_or_default("{oops", default={"x": 1}), {"x": 1})

    def test_empty_string(self):
        self.assertEqual(load_or_default("", default=[]), [])

    def test_default_is_none_by_default(self):
        self.assertIsNone(load_or_default("not json"))

    def test_none_is_a_type_error(self):
        with self.assertRaises(TypeError):
            load_or_default(None, default={})

    def test_int_is_a_type_error(self):
        with self.assertRaises(TypeError):
            load_or_default(42, default={})


if __name__ == "__main__":
    unittest.main()
