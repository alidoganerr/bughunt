import unittest

from solution import check_rows


class CheckRowsTest(unittest.TestCase):
    def test_all_valid(self):
        rows = [{"name": "a", "qty": 1}, {"name": "b"}]
        self.assertEqual(check_rows(rows), [])

    def test_empty_input(self):
        self.assertEqual(check_rows([]), [])

    def test_single_missing_name(self):
        self.assertEqual(check_rows([{"name": ""}]), ["row 1: missing name"])

    def test_several_negative_quantities(self):
        rows = [{"name": "a", "qty": -1}, {"name": "b", "qty": 2}, {"name": "c", "qty": -3}]
        self.assertEqual(
            check_rows(rows), ["row 1: negative qty", "row 3: negative qty"]
        )

    def test_keeps_going_after_missing_name(self):
        rows = [{"name": ""}, {"name": "b", "qty": -2}]
        self.assertEqual(
            check_rows(rows), ["row 1: missing name", "row 2: negative qty"]
        )

    def test_one_row_with_both_problems(self):
        rows = [{"qty": -1}]
        self.assertEqual(
            check_rows(rows), ["row 1: missing name", "row 1: negative qty"]
        )

    def test_missing_name_key(self):
        rows = [{"name": "a"}, {"qty": 5}]
        self.assertEqual(check_rows(rows), ["row 2: missing name"])


if __name__ == "__main__":
    unittest.main()
