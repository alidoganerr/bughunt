"""Grid helpers. A grid is a list of row lists."""


def with_cell(grid, row, col, value):
    """Return a copy of grid with grid[row][col] replaced by value."""
    if not 0 <= row < len(grid) or not 0 <= col < len(grid[row]):
        raise IndexError("cell is outside the grid")
    new_grid = [list(r) for r in grid]
    new_grid[row][col] = value
    return new_grid
