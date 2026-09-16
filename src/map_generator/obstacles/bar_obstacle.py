from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.grid_randomizer import GridRandomizer


class BarObstacle(ObstacleStrategy):
    """
    Strategy that generates a linear block of obstacles (horizontal or vertical).
    The bar has a randomized length (3 to 15 cells) and thickness (1 to 3 cells).
    """

    @property
    def name(self) -> str:
        return "Bar"

    def apply(self, grid: Grid, rand: GridRandomizer, config: GeneratorConfig):
        x = rand.next_int(0, grid.width)
        y = rand.next_int(0, grid.height)
        is_horizontal = rand.next_bool()
        length = rand.next_int(3, 15)
        size = rand.next_int(1, 4)

        for _ in range(size):
            for i in range(length):
                if is_horizontal:
                    grid.set_obstacle(x + i, y)
                else:
                    grid.set_obstacle(x, y + i)
            if is_horizontal:
                y += 1
            else:
                x += 1
