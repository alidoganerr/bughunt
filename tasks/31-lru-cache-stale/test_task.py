import unittest

from solution import Settings


class SettingsTest(unittest.TestCase):
    def test_initial_values(self):
        self.assertEqual(Settings({"a": 1}).get("a"), 1)

    def test_missing_key(self):
        with self.assertRaises(KeyError):
            Settings().get("nope")

    def test_set_new_key(self):
        s = Settings()
        s.set("a", 1)
        self.assertEqual(s.get("a"), 1)

    def test_set_after_failed_get(self):
        s = Settings()
        with self.assertRaises(KeyError):
            s.get("a")
        s.set("a", 2)
        self.assertEqual(s.get("a"), 2)

    def test_objects_are_independent(self):
        first = Settings({"mode": "fast"})
        second = Settings({"mode": "safe"})
        self.assertEqual(first.get("mode"), "fast")
        self.assertEqual(second.get("mode"), "safe")

    def test_passed_dict_is_copied(self):
        source = {"a": 1}
        s = Settings(source)
        source["a"] = 99
        self.assertEqual(s.get("a"), 1)

    def test_overwrite_is_visible(self):
        s = Settings({"mode": "fast"})
        self.assertEqual(s.get("mode"), "fast")
        s.set("mode", "safe")
        self.assertEqual(s.get("mode"), "safe")

    def test_repeated_overwrites(self):
        s = Settings()
        for n in range(3):
            s.set("n", n)
            self.assertEqual(s.get("n"), n)


if __name__ == "__main__":
    unittest.main()
