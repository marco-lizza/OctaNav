from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.agglomerate_obstacle import AgglomerateObstacle
from map_generator.obstacles.bar_obstacle import BarObstacle
from map_generator.obstacles.diagonal_obstacle import DiagonalObstacle
from map_generator.obstacles.enclosure__obstacle import EnclosureObstacle
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.obstacles.random_obstacle import RandomObstacle
from map_generator.utils.grid_randomizer import GridRandomizer


class GridGenerator:
    """
    Orchestrates the map generation process.
    It initializes the grid and applies various obstacle generation strategies
    based on the provided configuration.

    Attributes:
        strategies (list[ObstacleStrategy]): A list of all available obstacle
            generation strategies registered in the system.
    """

    def __init__(self):
        """
        Initializes the GridGenerator and registers all available obstacle strategies.
        """
        self.strategies: list[ObstacleStrategy] = [
            RandomObstacle(),
            BarObstacle(),
            EnclosureObstacle(),
            DiagonalObstacle(),
            AgglomerateObstacle(),
        ]

    def generate_map(self, config: GeneratorConfig) -> Grid:
        """
        Generates a new grid map based on the provided configuration settings.
        Iterates through registered strategies and applies them the specified
        number of times.

        Args:
            config (GeneratorConfig): The configuration containing grid dimensions,
                seed, and obstacle counts.

        Returns:
            Grid: The fully generated grid map populated with obstacles.
        """
        grid = Grid(config.width, config.height)
        rand = GridRandomizer(config.seed)

        for strategy in self.strategies:
            count = config.obstacle_counts.get(strategy.name, 0)
            for _ in range(count):
                strategy.apply(grid, rand, config)

        return grid
