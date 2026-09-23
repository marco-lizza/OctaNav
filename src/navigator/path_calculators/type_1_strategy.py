from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.path_calculators.i_path_strategy import IPathStrategy


class Type1Strategy(IPathStrategy):
    """
    Strategy to compute a Type 1 free path (Diagonal -> Orthogonal).
    """

    def compute(
        self, grid: Grid, origin: Coordinate, destination: Coordinate
    ) -> list[Coordinate] | None:
        path = [origin]
        current_x, current_y = origin.x, origin.y
        step_x = self._sign(destination.x - origin.x)
        step_y = self._sign(destination.y - origin.y)

        dx = abs(destination.x - origin.x)
        dy = abs(destination.y - origin.y)
        d_min = min(dx, dy)

        # 1. Diagonal Phase
        for _ in range(d_min):
            current_x += step_x
            current_y += step_y
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        # 2. Orthogonal Phase
        while current_x != destination.x:
            current_x += step_x
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        while current_y != destination.y:
            current_y += step_y
            if not grid.is_traversable(current_x, current_y):
                return None
            path.append(Coordinate(current_x, current_y))

        return path
