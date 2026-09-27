"""
Interface definition for map visualization strategies.

This module provides the IGridPrinter abstract base class, which establishes
the contract for any component responsible for rendering the map and its
associated navigation data (paths, areas, and obstacles).
"""

from abc import ABC, abstractmethod

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.util.base_printer_settings import BasePrinterSettings


class IGridPrinter(ABC):
    """
    Abstract base class defining the contract for grid visualization strategies.
    """

    def __init__(self, grid: Grid, settings: BasePrinterSettings) -> None:
        """
        Initialize the printer with the map and the view settings.

        Args:
            grid (Grid): The map model containing spatial constraints and obstacles.
            settings (BasePrinterSettings): View settings.
        """
        self.grid = grid
        self.settings = settings

    @abstractmethod
    def print_map(self) -> None:
        """
        Renders the base grid without any navigational overlays.

        This method is typically used to display the raw environment containing
        only traversable cells and obstacles, prior to any pathfinding operations.
        """

    @abstractmethod
    def print_areas(
        self,
        areas: list[
            tuple[str, list[Coordinate], list[tuple[str, list[Coordinate], int]], int]
        ],
    ) -> None:
        """
        Renders specific areas over the grid based on their integer ID.

        Args:
            areas (list[tuple[list[Coordinate],str, int]]): A list of tuple. Name of the area and view rendering settings of it.
        """
