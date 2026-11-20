import unittest

from solution import parse_header


class ParseHeaderTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_header("Host: example.com"), ("host", "example.com"))

    def test_extra_whitespace(self):
        self.assertEqual(parse_header("  Accept :  text/html  "), ("accept", "text/html"))

    def test_empty_value(self):
        self.assertEqual(parse_header("X-Empty:"), ("x-empty", ""))

    def test_colon_in_value(self):
        self.assertEqual(
            parse_header("Host: example.com:8080"), ("host", "example.com:8080")
        )

    def test_time_value(self):
        self.assertEqual(parse_header("Time: 12:30:45"), ("time", "12:30:45"))

    def test_no_colon(self):
        with self.assertRaises(ValueError):
            parse_header("not a header")


if __name__ == "__main__":
    unittest.main()
