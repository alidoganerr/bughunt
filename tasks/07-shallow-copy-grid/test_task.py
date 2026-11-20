import unittest

from solution import with_cell


class WithCellTest(unittest.TestCase):
    def test_result(self):
        self.assertEqual(with_cell([[1, 2], [3, 4]], 1, 0, 9), [[1, 2], [9, 4]])

    def test_original_unchanged(self):
        grid = [[1, 2], [3, 4]]
        with_cell(grid, 0, 1, 9)
        self.assertEqual(grid, [[1, 2], [3, 4]])

    def test_rows_are_not_shared(self):
        grid = [[1, 2], [3, 4]]
        new = with_cell(grid, 0, 0, 7)
        new[1][1] = 99
        self.assertEqual(grid[1], [3, 4])

    def test_row_out_of_range(self):
        with self.assertRaises(IndexError):
            with_cell([[1]], 1, 0, 5)

    def test_col_out_of_range(self):
        with self.assertRaises(IndexError):
            with_cell([[1, 2]], 0, 2, 5)

    def test_negative_index(self):
        with self.assertRaises(IndexError):
            with_cell([[1, 2], [3, 4]], -1, 0, 5)
        with self.assertRaises(IndexError):
            with_cell([[1, 2], [3, 4]], 0, -1, 5)

    def test_ragged_grid(self):
        self.assertEqual(with_cell([[1], [2, 3]], 1, 1, 0), [[1], [2, 0]])


if __name__ == "__main__":
    unittest.main()
