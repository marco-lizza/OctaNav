from map_generator.config.config import GeneratorConfig
from map_generator.models.coordinate import Coordinate
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

    def __init__(self, config: GeneratorConfig):
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
        self.config = config

    def generate_map(self, seed: int) -> Grid:
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
        grid = Grid(self.config.width, self.config.height)
        rand = GridRandomizer(seed)

        for strategy in self.strategies:
            count = self.config.obstacle_counts.get(strategy.name, 0)
            for _ in range(count):
                strategy.apply(grid, rand, self.config)

        return grid

    def generate_origin_and_destination(
        self, grid: Grid, seed: int
    ) -> tuple[Coordinate, Coordinate]:
        """
        Generates a valid, distinct origin and destination pair.
        Both points are guaranteed to be on traversable cells (not obstacles).

        Args:
            grid (Grid): The map model to generate points for.
            seed (int): The seed used to initialize the randomizer for reproducibility.

        Returns:
            tuple[Coordinate, Coordinate]: A tuple containing the origin
                and destination coordinate.
        """
        rand = GridRandomizer(seed)

        while True:
            ox = rand.next_int(0, grid.width)
            oy = rand.next_int(0, grid.height)

            if grid.is_traversable(ox, oy):
                origin = Coordinate(ox, oy)
                break

        while True:
            dx = rand.next_int(0, grid.width)
            dy = rand.next_int(0, grid.height)

            if grid.is_traversable(dx, dy) and (dx, dy) != origin:
                destination = Coordinate(dx, dy)
                break

        return origin, destination
