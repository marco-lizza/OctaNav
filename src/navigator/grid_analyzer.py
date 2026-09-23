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

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Skip non-traversable cells completely
                if not self.grid.is_traversable(x, y):
                    continue

                target = Coordinate(x, y)

                # The origin is trivially reachable from itself (null path, Type 1)
                if target.x == origin.x and target.y == origin.y:
                    context.add(target)
                    continue

                # Get all paths from the engine (memoized)
                result = self.engine.get_paths_and_distance(origin, target)

                # 1. Check for Type 1 Free Path (Context)
                if result.type_1_path is not None:
                    context.add(target)
                    continue  # If it's in Context, it CANNOT be in Complement

                # 2. Check for Type 2 Free Path (Complement)
                if result.type_2_path is not None:
                    complement.add(target)

        return AnalysisResult(context=context, complement=complement)
