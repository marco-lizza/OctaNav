import math

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.models.analysis_result import AnalysisResult
from navigator.path_engine import PathEngine


class GridAnalyzer:
    """
    Analyzer responsible for scanning the entire grid to classify cells
    into Context and Complement relative to a specific Origin cell.
    """

    def __init__(self, grid: Grid, engine: PathEngine):
        """
        Initializes the GridAnalyzer.

        Args:
            grid (Grid): The map model to analyze.
            engine (PathEngine): The engine used to evaluate free paths.
        """
        self.grid = grid
        self.engine = engine

    def analyze_origin(self, origin: Coordinate) -> AnalysisResult:
        """
        Scans all cells in the grid to determine the Context and Complement
        for the given origin cell.

        Domain Rules applied:
        - Context: Reachable via Type 1 path.
        - Complement: Reachable via Type 2 path, BUT NOT by Type 1.

        Args:
            origin (Coordinate): The starting cell (O).

        Returns:
            AnalysisResult: An object containing the sets of Context and Complement cells.
        """
        context: set[Coordinate] = set()
        complement: set[Coordinate] = set()
        border: dict[Coordinate, int] = {}
        excluded: set[Coordinate] = set()

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if not self.grid.is_traversable(x, y):
                    continue

                target = Coordinate(x, y)

                if target.x == origin.x and target.y == origin.y:
                    context.add(target)
                    continue

                result = self.engine.get_paths_and_distance(origin, target)

                if result.type_1_path is not None:
                    context.add(target)
                    continue

                if result.type_2_path is not None:
                    complement.add(target)
                    continue

                excluded.add(target)

        for cell in excluded:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    neighbor = Coordinate(cell.x + dx, cell.y + dy)

                    if neighbor in context:
                        border[neighbor] = 1
                    if neighbor in complement:
                        border[neighbor] = 2

        return AnalysisResult(
            context=context, complement=complement, border=border, excluded=excluded
        )

    def cammino_min(
        self,
        origin: Coordinate,
        destination: Coordinate,
        grid: Grid,
        stats: dict[str, int],
        _is_top_level: bool = True,
    ) -> tuple[float, list[tuple[Coordinate, int]]]:
        """
        Calculates the shortest path (minimum path) between the origin and the destination
        using a recursive boundary-exploration algorithm.

        The algorithm checks if the destination is immediately reachable within the current
        Context or Complement. If not, it recursively explores the border cells (the frontier
        between reachable areas and excluded areas), treating previously explored areas
        as obstacles to prevent backtracking, and attempts to reach the destination from there.

        Args:
            origin (Coordinate): The starting cell for the current path segment.
            destination (Coordinate): The final target cell.
            grid (Grid): The map model, which is temporarily mutated during the recursive
                steps to block backtracking.
            stats (dict[str, int]): Dictionary passed by reference to track execution statistics.

        Returns:
            tuple[float, list[tuple[Coordinate, int]]]: A tuple containing:
                - float: The total minimum theoretical distance (cost) of the path.
                - list[tuple[Coordinate, int]]: The sequence of landmark coordinates and
                  their corresponding path type identifier (e.g., 0 for Origin, 1 for Context,
                  2 for Complement). Returns math.inf and an empty list if no path is found.
        """
        if _is_top_level:
            stats["interrupted"] = False

        try:
            analysis_result = self.analyze_origin(origin)

            if destination in analysis_result.context:
                stats["paths_found"] += 1
                print(
                    f"\r[INFO] Valid paths found so far: {stats['paths_found']}",
                    end="",
                    flush=True,
                )
                return (
                    self.engine._compute_theoretical_dlib(origin, destination),
                    [(origin, 0), (destination, 1)],
                )

            if destination in analysis_result.complement:
                stats["paths_found"] += 1
                print(
                    f"\r[INFO] Valid paths found so far: {stats['paths_found']}",
                    end="",
                    flush=True,
                )
                return (
                    self.engine._compute_theoretical_dlib(origin, destination),
                    [(origin, 0), (destination, 2)],
                )

            if len(analysis_result.border) == 0:
                return math.inf, []

            stats["border_cells"] += len(analysis_result.border)

            lenght_min = math.inf
            seq_min = []

            for cell in analysis_result.border:
                lF = self.engine._compute_theoretical_dlib(origin, cell)

                if lF < lenght_min:
                    for complement_cell in analysis_result.complement:
                        grid.set_obstacle(complement_cell.x, complement_cell.y)
                    for context_cell in analysis_result.context:
                        grid.set_obstacle(context_cell.x, context_cell.y)

                    try:
                        lFD, seqFD = self.cammino_min(
                            cell, destination, grid, stats, _is_top_level=False
                        )
                    finally:
                        for complement_cell in analysis_result.complement:
                            grid.remove_obstacle(complement_cell.x, complement_cell.y)
                        for context_cell in analysis_result.context:
                            grid.remove_obstacle(context_cell.x, context_cell.y)

                    lTot = lF + lFD

                    if lTot < lenght_min:
                        lenght_min = lTot
                        seq_min = [
                            (origin, 0),
                            (cell, analysis_result.border[cell]),
                        ] + seqFD[1:]
                else:
                    stats["condition_false"] += 1

            return (lenght_min, seq_min)

        except KeyboardInterrupt:
            stats["interrupted"] = True
            if _is_top_level:
                return (lenght_min, seq_min)
            raise
