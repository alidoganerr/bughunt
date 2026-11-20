import unittest

from solution import sort_versions


class SortVersionsTest(unittest.TestCase):
    def test_single_digit_parts(self):
        self.assertEqual(
            sort_versions(["1.2.0", "1.0.5", "0.9.9"]),
            ["0.9.9", "1.0.5", "1.2.0"],
        )

    def test_two_digit_minor(self):
        self.assertEqual(
            sort_versions(["1.10.0", "1.2.0", "1.9.5"]),
            ["1.2.0", "1.9.5", "1.10.0"],
        )

    def test_two_digit_major(self):
        self.assertEqual(sort_versions(["10.0.0", "9.0.0"]), ["9.0.0", "10.0.0"])

    def test_patch_numbers(self):
        self.assertEqual(
            sort_versions(["1.0.10", "1.0.9", "1.0.100"]),
            ["1.0.9", "1.0.10", "1.0.100"],
        )

    def test_v_prefix_is_kept(self):
        self.assertEqual(
            sort_versions(["v2.0.0", "1.9.0", "v1.10.0"]),
            ["1.9.0", "v1.10.0", "v2.0.0"],
        )

    def test_empty(self):
        self.assertEqual(sort_versions([]), [])

    def test_input_not_modified(self):
        data = ["2.0.0", "1.0.0"]
        sort_versions(data)
        self.assertEqual(data, ["2.0.0", "1.0.0"])


if __name__ == "__main__":
    unittest.main()
