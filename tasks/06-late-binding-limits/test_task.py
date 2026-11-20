import unittest

from solution import build_checks


class BuildChecksTest(unittest.TestCase):
    def test_single_limit(self):
        checks = build_checks({"cpu": 80})
        self.assertIs(checks["cpu"](50), True)
        self.assertIs(checks["cpu"](81), False)

    def test_boundary_is_allowed(self):
        checks = build_checks({"cpu": 80})
        self.assertIs(checks["cpu"](80), True)

    def test_each_check_uses_its_own_limit(self):
        checks = build_checks({"cpu": 80, "memory": 10})
        self.assertIs(checks["cpu"](50), True)
        self.assertIs(checks["memory"](50), False)

    def test_three_limits(self):
        checks = build_checks({"a": 1, "b": 5, "c": 9})
        self.assertEqual([checks[k](4) for k in "abc"], [False, True, True])

    def test_keys(self):
        self.assertEqual(sorted(build_checks({"x": 1, "y": 2})), ["x", "y"])

    def test_empty(self):
        self.assertEqual(build_checks({}), {})

    def test_negative_limit(self):
        with self.assertRaises(ValueError):
            build_checks({"ok": 1, "bad": -1})


if __name__ == "__main__":
    unittest.main()
