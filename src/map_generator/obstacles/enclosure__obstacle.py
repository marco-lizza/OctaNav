from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.grid_randomizer import GridRandomizer


class EnclosureObstacle(ObstacleStrategy):
    """
    Strategy that creates a closed rectangular perimeter of obstacles.
    This effectively partitions the grid, making the inner traversable cells
    unreachable from the outside area.
    """

    @property
    def name(self) -> str:
        return "Enclosure"

    def apply(self, grid: Grid, rand: GridRandomizer, config: GeneratorConfig):
        w = rand.next_int(4, 12)
        h = rand.next_int(4, 12)

        start_x = rand.next_int(0, max(1, grid.width - w))
        start_y = rand.next_int(0, max(1, grid.height - h))

        for i in range(w):
            grid.set_obstacle(start_x + i, start_y)  # Top
            grid.set_obstacle(start_x + i, start_y + h - 1)  # Bottom
        for j in range(h):
            grid.set_obstacle(start_x, start_y + j)  # Left
            grid.set_obstacle(start_x + w - 1, start_y + j)  # Right
