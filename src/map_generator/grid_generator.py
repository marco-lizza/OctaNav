from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.obstacles.bar_obstacle import BarObstacle
from map_generator.obstacles.diagonal_obstacle import DiagonalObstacle
from map_generator.obstacles.enclosure__obstacle import EnclosureObstacle
from map_generator.obstacles.obstacle_strategy import ObstacleStrategy
from map_generator.obstacles.random_obstacle import RandomObstacle
from map_generator.utils.Randomizer import Randomizer


class GridGenerator:
    def __init__(self):
        # Registrazione delle strategie disponibili
        self.strategies: list[ObstacleStrategy] = [
            RandomObstacle(),
            BarObstacle(),
            EnclosureObstacle(),
            DiagonalObstacle(),
            # Aggiungere qui le classi per Agglomerati e Linee Diagonali
        ]

    def generate_map(self, config: GeneratorConfig) -> Grid:
        grid = Grid(config.width, config.height)
        rand = Randomizer(config.seed)

        for strategy in self.strategies:
            count = config.obstacle_counts.get(strategy.name, 0)
            for _ in range(count):
                strategy.apply(grid, rand, config)

        return grid
