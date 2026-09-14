from map_generator.models.grid import Grid
from map_generator.ui.i_grid_printer import IGridPrinter


class ConsolePrinter(IGridPrinter):
    def print_map(self, grid: Grid) -> None:
        print(f"\n--- Mappa {grid.width}x{grid.height} ---")
        for y in range(grid.height):
            row = []
            for x in range(grid.width):
                row.append(". " if grid.cells[x][y].is_traversable else "█ ")
            print("".join(row))
        print("-------------------\n")
