import unittest

from solution import parse_csv


class ParseCsvTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_csv("a,b\n1,2\n"), [["a", "b"], ["1", "2"]])

    def test_crlf_rows(self):
        self.assertEqual(parse_csv("a,b\r\n1,2\r\n"), [["a", "b"], ["1", "2"]])

    def test_no_final_newline(self):
        self.assertEqual(parse_csv("a,b\n1,2"), [["a", "b"], ["1", "2"]])

    def test_quoted_comma(self):
        self.assertEqual(parse_csv('x,"a,b",y\n'), [["x", "a,b", "y"]])

    def test_doubled_quote(self):
        self.assertEqual(parse_csv('"say ""hi""",c\n'), [['say "hi"', "c"]])

    def test_empty_text(self):
        self.assertEqual(parse_csv(""), [])

    def test_empty_fields(self):
        self.assertEqual(parse_csv("a,,c\n"), [["a", "", "c"]])

    def test_blank_line_is_an_empty_row(self):
        self.assertEqual(parse_csv("a\n\nb\n"), [["a"], [], ["b"]])

    def test_newline_inside_quotes(self):
        text = 'id,note\r\n1,"first line\nsecond line"\r\n'
        self.assertEqual(
            parse_csv(text), [["id", "note"], ["1", "first line\nsecond line"]]
        )

    def test_crlf_inside_quotes_is_kept(self):
        self.assertEqual(parse_csv('a,"x\r\ny"\n'), [["a", "x\r\ny"]])


if __name__ == "__main__":
    unittest.main()
