from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.utils.grid_randomizer import GridRandomizer


class AgglomerateObstacle(ObstacleStrategy):
    """
    Strategy that generates a small contiguous cluster of non-traversable cells.
    Uses a random walk approach to place 2 to 4 orthogonally connected blocks.
    """

    @property
    def name(self) -> str:
        return "Agglomerate"

    def apply(self, grid: Grid, rand: GridRandomizer, config: GeneratorConfig):
        directions = {0: (0, -1), 1: (0, 1), 2: (1, 0), 3: (-1, 0)}
        cells_selected = set()
        x = rand.next_int(0, grid.width)
        y = rand.next_int(0, grid.height)
        grid.set_obstacle(x, y)
        cells_selected.add((x, y))

        size = rand.next_int(1, 3)
        agglomerate_actual_size = 0
        while agglomerate_actual_size < size:
            direction_selected = rand.next_int(0, 3)
            next_cell = (
                x + directions[direction_selected][0],
                y + directions[direction_selected][1],
            )
            if next_cell not in cells_selected:
                grid.set_obstacle(next_cell[0], next_cell[1])
                cells_selected.add(next_cell)
                agglomerate_actual_size += 1
                x = next_cell[0]
                y = next_cell[1]
