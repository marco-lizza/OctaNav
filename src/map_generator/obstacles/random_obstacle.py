from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.grid_randomizer import GridRandomizer


class RandomObstacle(ObstacleStrategy):
    """
    Strategy that places a single, isolated non-traversable cell
    at a random coordinate within the grid.
    """

    @property
    def name(self) -> str:
        return "Random"

    def apply(self, grid: Grid, rand: GridRandomizer, config: GeneratorConfig):
        x = rand.next_int(0, grid.width)
        y = rand.next_int(0, grid.height)
        grid.set_obstacle(x, y)
