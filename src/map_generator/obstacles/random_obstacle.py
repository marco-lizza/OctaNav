from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.Randomizer import Randomizer


class RandomObstacle(ObstacleStrategy):
    @property
    def name(self) -> str:
        return "Random"

    def apply(self, grid: Grid, rand: Randomizer, config: GeneratorConfig):
        x = rand.next_int(0, grid.width)
        y = rand.next_int(0, grid.height)
        grid.set_obstacle(x, y)
