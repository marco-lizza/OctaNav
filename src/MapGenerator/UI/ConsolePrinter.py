from MapGenerator.Models.Map import Map
from MapGenerator.UI.IGridPrinter import IGridPrinter


class ConsolePrinter(IGridPrinter):
    def print_map(self, map: Map) -> None:
        print(f"\n--- Mappa {map.width}x{map.height} ---")
        for y in range(map.height):
            row = []
            for x in range(map.width):
                row.append(". " if map.cells[x][y].is_traversable else "█ ")
            print("".join(row))
        print("-------------------\n")
