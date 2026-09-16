from map_generator.models.grid import Grid
from map_generator.ui.i_grid_printer import IGridPrinter


class ConsolePrinter(IGridPrinter):
    """
    Implementation of IGridPrinter that outputs the grid to the standard console.
    Uses ASCII/Unicode characters to represent traversable cells and obstacles.
    """

    def print_map(self, grid: Grid) -> None:
        """
        Prints the grid to the terminal.
        Traversable cells are represented by '. ' and obstacles by '█ '.

        Args:
            grid (Grid): The grid object to print.
        """
        print(f"\n--- Map {grid.width}x{grid.height} ---")
        for y in range(grid.height):
            row = []
            for x in range(grid.width):
                row.append(". " if grid.cells[x][y].is_traversable else "█ ")
            print("".join(row))
        print("-------------------\n")
