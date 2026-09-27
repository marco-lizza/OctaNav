"""
Command Line Interface (CLI) visualization strategy module.

This module provides the ConsolePrinter class, which implements the IGridPrinter
interface. It renders the grid and its navigational data directly to the standard
terminal using ASCII/Unicode characters.
"""

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.cli.cli_printer_settings import CLIPrinterSettings
from map_visualizer.i_grid_printer import IGridPrinter


class ConsolePrinter(IGridPrinter):
    """
    Implementation of IGridPrinter for the standard console.

    This printer visualizes the map by printing discrete layers sequentially.
    """

    def __init__(self, grid: Grid, settings: CLIPrinterSettings) -> None:
        """
        Initializes the console printer with the grid and visualization settings.
        """
        super().__init__(grid, settings)
        self.settings: CLIPrinterSettings = settings

    def _get_base_matrix(self) -> list[list[str]]:
        """
        Generates a 2D string matrix representing the bare environment.

        Returns:
            list[list[str]]: A 2D list where each element is a string character
                representing either a traversable cell or an obstacle.
        """
        matrix = []
        for y in range(self.grid.height):
            row = []
            for x in range(self.grid.width):
                if self.grid.is_traversable(x, y):
                    row.append(self.settings.empty_cell_char)
                else:
                    row.append(self.settings.obstacle_char)
            matrix.append(row)
        return matrix

    def print_map(self) -> None:
        """
        Prints the base grid to the standard output.
        """
        matrix = self._get_base_matrix()
        print(f"\n--- Map {self.grid.width}x{self.grid.height} ---")
        for row in matrix:
            print("".join(row))
        print("-------------------\n")

    def print_areas(
        self,
        areas: list[
            tuple[str, list[Coordinate], list[tuple[str, list[Coordinate], int]], int]
        ],
    ) -> None:
        """
        Renders specific areas and their point-of-interest groups sequentially to the terminal.

        Args:
            areas: List of tuples containing:
                - str: The name of the area (used as the title).
                - list[Coordinate]: The primary collection of cells making up the area.
                - list[tuple[str, list[Coordinate], int]]: Groups of Points of Interest
                  (POI group name, list of coordinates, style ID).
                - int: The ID used to look up the main area's drawing style in settings.
        """
        for name, coords, pois, area_id in areas:
            # Skip if there is absolutely nothing to draw
            if not coords and not pois:
                continue

            matrix = self._get_base_matrix()

            area_style = self.settings.area_styles.get(area_id, "? ")

            # Draw the main area cells
            for coord in coords:
                if 0 <= coord.y < self.grid.height and 0 <= coord.x < self.grid.width:
                    matrix[coord.y][coord.x] = area_style

            # Draw the Points of Interest (POIs) groups on top of the area cells
            poi_legends = []
            for poi_name, poi_coords, poi_id in pois:
                poi_style = self.settings.area_styles.get(poi_id, "! ")

                drawn_any = False
                for poi_coord in poi_coords:
                    if (
                        0 <= poi_coord.y < self.grid.height
                        and 0 <= poi_coord.x < self.grid.width
                    ):
                        matrix[poi_coord.y][poi_coord.x] = poi_style
                        drawn_any = True

                # Store the mapping for the legend just once per POI group
                if drawn_any:
                    legend_entry = f"{poi_style.strip()} = {poi_name}"
                    if legend_entry not in poi_legends:
                        poi_legends.append(legend_entry)

            # Print the resulting matrix
            print(f"\n--- {name} ---")
            for row in matrix:
                print("".join(row))

            # Print a small legend for the POIs if any exist in this area
            if poi_legends:
                print(f"Legend: {', '.join(poi_legends)}")

            print("-------------------\n")
