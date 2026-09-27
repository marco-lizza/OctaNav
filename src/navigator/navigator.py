from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.grid_analyzer import AnalysisResult, GridAnalyzer
from navigator.path_engine import FreePathResult, PathEngine


class Navigator:
    """
    Facade class for the navigation and pathfinding module.

    Provides a unified, high-level interface to interact with the underlying
    path calculators and grid analyzers without exposing their internal complexities.
    """

    def __init__(self, grid: Grid):
        """
        Initializes the Navigator with a specific map grid.

        Args:
            grid (Grid): The map model to navigate and analyze.
        """
        self.grid = grid
        self._engine = PathEngine(grid)
        self._analyzer = GridAnalyzer(grid, self._engine)

    def get_paths_and_distance(
        self, origin: Coordinate, destination: Coordinate
    ) -> FreePathResult:
        """
        Attempts to find free paths (Type 1 and 2) and the corresponding free
        distance between two cells using the underlying path engine.

        Args:
            origin (Coordinate): The starting cell.
            destination (Coordinate): The ending cell.

        Returns:
            FreePathResult: A DTO containing the paths and valid dlib (if any).
        """
        return self._engine.get_paths_and_distance(origin, destination)

    def analyze_context(self, origin: Coordinate) -> AnalysisResult:
        """
        Analyzes the entire grid to find all reachable cells from the origin
        via free paths (Context and Complement).

        Args:
            origin (Coordinate): The starting cell.

        Returns:
            AnalysisResult: A DTO containing the sets of Context and Complement cells.
        """
        return self._analyzer.analyze_origin(origin)

    def get_path(
        self,
        origin: Coordinate,
        destination: Coordinate,
        grid: Grid,
        use_heuristic: bool = False,
        use_sorting: bool = False,
    ) -> tuple[float, list[tuple[Coordinate, int]], dict[str, int]]:
        """
        Calculates the shortest theoretical path between the origin and the destination
        by delegating to the grid analyzer's minimum path algorithm, while tracking stats.

        Args:
            origin (Coordinate): The starting cell.
            destination (Coordinate): The target destination cell.
            grid (Grid): The map model to be navigated (may be temporarily mutated
                during the internal recursive evaluation).

        Returns:
            tuple[float, list[tuple[Coordinate, int]], dict]: A tuple containing:
                - float: The total minimum distance (cost) of the path.
                - list[tuple[Coordinate, int]]: The sequence of landmark coordinates
                  and their corresponding path type identifiers.
                - dict[str, int]: Execution statistics (border cells evaluated, skips).
        """
        stats = {
            "border_cells": 0,
            "condition_false": 0,
            "paths_found": 0,
            "interrupted": False,
        }

        cost, path = self._analyzer.cammino_min(
            origin, destination, grid, stats, use_heuristic, use_sorting
        )
        print()

        if stats["interrupted"]:
            print(
                "[WARNING] Calculation interrupted by the user! Returning best path found so far."
            )

        return cost, path, stats

    def get_path_from_landmarks(
        self, landmarks: list[tuple[Coordinate, int]]
    ) -> list[Coordinate]:
        """
        Reconstructs the full, continuous sequence of cell coordinates that make up
        a path, based on a given sequence of key landmarks.

        Args:
            landmarks (list[tuple[Coordinate, int]]): The sequence of landmark
                coordinates and their path type identifiers (e.g., the sequence
                returned by get_path).

        Returns:
            list[Coordinate]: The complete list of coordinates forming the continuous
                path from start to finish.
        """
        return self._engine.get_path_from_landmarks(landmarks)
