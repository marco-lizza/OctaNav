"""
Interface definition for map visualization strategies.

This module provides the IGridPrinter abstract base class, which establishes
the contract for any component responsible for rendering the map and its
associated navigation data (paths, areas, and obstacles).
"""

from abc import ABC, abstractmethod

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.grid_analyzer import AnalysisResult
from navigator.path_engine import FreePathResult


class IGridPrinter(ABC):
    """
    Abstract base class defining the contract for grid visualization strategies.

    Any concrete implementation (e.g., console-based or GUI-based printers)
    must inherit from this class. It enforces a declarative rendering approach:
    the caller provides the full state of the map and its analytical layers,
    and the concrete implementation decides how best to present it to the user.
    """

    @abstractmethod
    def print_map(self, grid: Grid) -> None:
        """
        Renders the base grid without any navigational overlays.

        This method is typically used to display the raw environment containing
        only traversable cells and obstacles, prior to any pathfinding operations.

        Args:
            grid (Grid): The map model containing spatial constraints and obstacles.
        """

    @abstractmethod
    def print_analysis(
        self,
        grid: Grid,
        origin: Coordinate,
        dest: Coordinate,
        analysis: AnalysisResult,
        paths: FreePathResult,
    ) -> None:
        """
        Renders the complete navigation analysis over the grid.

        This method receives the full navigational state and overlays it onto
        the base map. The specific implementation dictates the presentation logic
        (e.g., printing discrete static layers sequentially in a CLI environment,
        or rendering an interactive MVC dashboard in a GUI).

        Args:
            grid (Grid): The core map model containing obstacles and boundaries.
            origin (Coordinate): The starting point of the navigation.
            dest (Coordinate): The target destination of the navigation.
            analysis (AnalysisResult): DTO containing the Context and Complement
                coordinate sets.
            paths (FreePathResult): DTO containing the calculated Type 1 and Type 2
                paths, along with the theoretical free distance (dlib).
        """
