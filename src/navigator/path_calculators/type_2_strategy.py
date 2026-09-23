from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.path_calculators.i_path_strategy import IPathStrategy


class Type2Strategy(IPathStrategy):
    """
    Strategy to compute a Type 2 free path (Orthogonal -> Diagonal).
    Excludes purely straight or purely diagonal paths.
    """

    def compute(
        self, grid: Grid, origin: Coordinate, destination: Coordinate
    ) -> list[Coordinate] | None:
        dx = abs(destination.x - origin.x)
        dy = abs(destination.y - origin.y)

        # Pure paths are strictly Type 1 by domain rules
        if dx == 0 or dy == 0 or dx == dy:
            return None

        path = [origin]
        current_x, current_y = origin.x, origin.y
        step_x = self._sign(destination.x - origin.x)
        step_y = self._sign(destination.y - origin.y)

        d_min = min(dx, dy)
        ortho_x = dx - d_min
        ortho_y = dy - d_min

        # 1. Orthogonal Phase
        for _ in range(ortho_x):
            current_x += step_x
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        for _ in range(ortho_y):
            current_y += step_y
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        # 2. Diagonal Phase
        for _ in range(d_min):
            current_x += step_x
            current_y += step_y
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        return path
