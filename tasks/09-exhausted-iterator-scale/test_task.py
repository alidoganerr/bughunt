import unittest

from solution import scale_to_unit


class ScaleToUnitTest(unittest.TestCase):
    def test_list(self):
        self.assertEqual(scale_to_unit([1, 2, 4]), [0.25, 0.5, 1.0])

    def test_tuple(self):
        self.assertEqual(scale_to_unit((5, 10)), [0.5, 1.0])

    def test_empty(self):
        self.assertEqual(scale_to_unit([]), [])

    def test_empty_generator(self):
        self.assertEqual(scale_to_unit(v for v in []), [])

    def test_all_zero_list(self):
        self.assertEqual(scale_to_unit([0, 0]), [0.0, 0.0])

    def test_generator(self):
        self.assertEqual(scale_to_unit(v for v in [1, 2, 4]), [0.25, 0.5, 1.0])

    def test_iterator_all_zero(self):
        self.assertEqual(scale_to_unit(iter([0, 0, 0])), [0.0, 0.0, 0.0])

    def test_returns_floats(self):
        self.assertTrue(all(isinstance(v, float) for v in scale_to_unit([2, 2])))


if __name__ == "__main__":
    unittest.main()
