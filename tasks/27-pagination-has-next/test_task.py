import unittest

from solution import paginate


class PaginateTest(unittest.TestCase):
    def test_first_page_has_next(self):
        self.assertEqual(
            paginate([1, 2, 3, 4, 5], 1, 2),
            {"items": [1, 2], "page": 1, "pages": 3, "has_next": True},
        )

    def test_partial_last_page(self):
        self.assertEqual(
            paginate([1, 2, 3, 4, 5], 3, 2),
            {"items": [5], "page": 3, "pages": 3, "has_next": False},
        )

    def test_exactly_full_last_page(self):
        self.assertEqual(
            paginate([1, 2, 3, 4], 2, 2),
            {"items": [3, 4], "page": 2, "pages": 2, "has_next": False},
        )

    def test_single_full_page(self):
        result = paginate([1, 2, 3], 1, 3)
        self.assertEqual(result["pages"], 1)
        self.assertIs(result["has_next"], False)

    def test_empty(self):
        self.assertEqual(
            paginate([], 1, 10),
            {"items": [], "page": 1, "pages": 0, "has_next": False},
        )

    def test_page_past_the_end(self):
        self.assertEqual(
            paginate([1, 2, 3], 5, 2),
            {"items": [], "page": 5, "pages": 2, "has_next": False},
        )

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            paginate([1], 0, 5)
        with self.assertRaises(ValueError):
            paginate([1], 1, 0)


if __name__ == "__main__":
    unittest.main()
