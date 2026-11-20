import unittest

from solution import find_city


class FindCityTest(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(find_city(["Berlin", "Bonn"], "Bonn"), "Bonn")

    def test_ignores_case(self):
        self.assertEqual(find_city(["Berlin", "Bonn"], "bERLIN"), "Berlin")

    def test_strips_whitespace(self):
        self.assertEqual(find_city(["Berlin"], "  berlin\t"), "Berlin")
        self.assertEqual(find_city([" Berlin "], "BERLIN"), " Berlin ")

    def test_not_found(self):
        self.assertIsNone(find_city(["Berlin"], "Hamburg"))

    def test_first_match_wins(self):
        self.assertEqual(find_city(["Ulm", "ULM"], "ulm"), "Ulm")

    def test_german_sharp_s(self):
        cities = ["Berlin", "Weißenburg"]
        self.assertEqual(find_city(cities, "WEISSENBURG"), "Weißenburg")

    def test_sharp_s_in_the_list(self):
        self.assertEqual(find_city(["STRASSBURG"], "Straßburg"), "STRASSBURG")


if __name__ == "__main__":
    unittest.main()
