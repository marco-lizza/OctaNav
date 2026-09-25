"""
Command Line Interface (CLI) visualization strategy module.

This module provides the ConsolePrinter class, which implements the IGridPrinter
interface. It renders the grid and its navigational data directly to the standard
terminal using ASCII/Unicode characters.
"""

from collections.abc import Iterable

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.i_grid_printer import IGridPrinter
from navigator.grid_analyzer import AnalysisResult
from navigator.path_engine import FreePathResult


class ConsolePrinter(IGridPrinter):
    """
    Implementation of IGridPrinter for the standard console.

    This printer visualizes the map by printing discrete layers sequentially.
    Since a terminal cannot easily overlap multiple colors or interactive layers
    like a GUI, this class extracts each piece of analytical data (e.g., Context,
    Complement, Paths) and prints a dedicated text-based map for each one.
    """

    def _get_base_matrix(self, grid: Grid) -> list[list[str]]:
        """
        Generates a 2D string matrix representing the bare environment.

        Args:
            grid (Grid): The map model containing spatial constraints.

        Returns:
            list[list[str]]: A 2D list where each element is a string character
                representing either a traversable cell ('. ') or an obstacle ('█ ').
        """
        matrix = []
        for y in range(grid.height):
            row = []
            for x in range(grid.width):
                row.append(". " if grid.is_traversable(x, y) else "█ ")
            matrix.append(row)
        return matrix

    def print_map(self, grid: Grid) -> None:
        """
        Prints the base grid to the standard output.

        Args:
            grid (Grid): The map model to print.
        """
        matrix = self._get_base_matrix(grid)
        print(f"\n--- Map {grid.width}x{grid.height} ---")
        for row in matrix:
            print("".join(row))
        print("-------------------\n")

    def _print_layer(
        self, grid: Grid, title: str, cells: Iterable[Coordinate], style: str
    ) -> None:
        """
        Overlays a specific set of coordinates onto the base matrix and prints it.

        Args:
            grid (Grid): The map model used to generate the base layout.
            title (str): The header text to print above this specific map layer.
            cells (Iterable[Coordinate]): The collection of coordinates to highlight.
            style (str): The string character(s) used to mark the highlighted cells.
        """
        if not cells:
            return

        matrix = self._get_base_matrix(grid)
        for coord in cells:
            matrix[coord.y][coord.x] = f"{style} "

        print(f"\n--- {title} ---")
        for row in matrix:
            print("".join(row))

    def print_analysis(
        self,
        grid: Grid,
        origin: Coordinate,
        dest: Coordinate,
        analysis: AnalysisResult,
        paths: FreePathResult,
    ) -> None:
        """
        Prints the complete navigation analysis sequentially to the terminal.

        Renders separate maps for the Context area, the Complement area,
        the Type 1 path, and the Type 2 path, provided they exist.

        Args:
            grid (Grid): The map model.
            origin (Coordinate): The starting cell.
            dest (Coordinate): The destination cell.
            analysis (AnalysisResult): Context and Complement data sets.
            paths (FreePathResult): Type 1 and Type 2 paths data.
        """
        # Context
        self._print_layer(grid, "Context Area", analysis.context, "C")

        # Complement
        self._print_layer(grid, "Complement Area", analysis.complement, "K")

        closure = analysis.context
        closure.update(analysis.context)

        # Closure
        self._print_layer(grid, "Closure Area", closure, "C")

        # Border
        self._print_layer(grid, "Border Area", analysis.border, "B")

        # Paths
        if paths.type_1_path:
            self._print_layer(
                grid, "Type 1 Path (O=Origin, D=Dest)", paths.type_1_path, "*"
            )

        if paths.type_2_path:
            self._print_layer(
                grid, "Type 2 Path (O=Origin, D=Dest)", paths.type_2_path, "+"
            )
