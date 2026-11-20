# Replace one cell

Write `with_cell(grid, row, col, value)` in `solution.py`. `grid` is a list of rows and each row is a list. Return a new grid that equals `grid` except that the cell at `row`, `col` holds `value`.

- Neither `grid` nor any of its rows is modified.
- The returned grid shares no row list with `grid`, so changing the result later never changes the original.
- `row` and `col` must be inside the grid. Negative indexes count as out of range. Otherwise raise `IndexError`.

## Example

```python
>>> grid = [[1, 2], [3, 4]]
>>> new = with_cell(grid, 0, 1, 9)
>>> new
[[1, 9], [3, 4]]
>>> grid
[[1, 2], [3, 4]]
```
