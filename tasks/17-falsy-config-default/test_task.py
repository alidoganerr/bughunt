import unittest

from solution import get_setting


class GetSettingTest(unittest.TestCase):
    def test_present(self):
        self.assertEqual(get_setting({"name": "x"}, "name", "y"), "x")

    def test_missing_uses_default(self):
        self.assertEqual(get_setting({"a": 1}, "b", 7), 7)

    def test_missing_without_default(self):
        self.assertIsNone(get_setting({}, "b"))

    def test_zero_is_kept(self):
        self.assertEqual(get_setting({"retries": 0}, "retries", 3), 0)

    def test_false_is_kept(self):
        self.assertIs(get_setting({"debug": False}, "debug", True), False)

    def test_empty_string_is_kept(self):
        self.assertEqual(get_setting({"prefix": ""}, "prefix", "app_"), "")

    def test_empty_list_is_kept(self):
        self.assertEqual(get_setting({"hosts": []}, "hosts", ["localhost"]), [])

    def test_none_is_kept(self):
        self.assertIsNone(get_setting({"proxy": None}, "proxy", "direct"))


if __name__ == "__main__":
    unittest.main()
