from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.Randomizer import Randomizer


class DiagonalObstacle(ObstacleStrategy):
    @property
    def name(self) -> str:
        return "Diagonal"

    def apply(self, grid: Grid, rand: Randomizer, config: GeneratorConfig):
        directions = {0: (1, -1), 1: (-1, -1), 2: (-1, 1), 3: (-1, -1)}
        x = rand.next_int(0, grid.width)
        y = rand.next_int(0, grid.height)
        direction_selected = rand.next_int(0, 3)
        length = rand.next_int(3, 15)
        print(length)

        for _ in range(length):
            grid.set_obstacle(x, y)
            x += directions[direction_selected][0]
            y += directions[direction_selected][1]
