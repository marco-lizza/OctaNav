from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Models.Map import Map
from MapGenerator.Obstacles.BarObstacle import BarObstacle
from MapGenerator.Obstacles.EnclosureObstacle import EnclosureObstacle
from MapGenerator.Obstacles.ObstacleStrategy import ObstacleStrategy
from MapGenerator.Obstacles.RandomObstacle import RandomObstacle
from MapGenerator.Utils.Randomizer import Randomizer


class Generator:
    def __init__(self):
        # Registrazione delle strategie disponibili
        self.strategies: list[ObstacleStrategy] = [
            RandomObstacle(),
            BarObstacle(),
            EnclosureObstacle(),
            # Aggiungere qui le classi per Agglomerati e Linee Diagonali
        ]

    def generate_map(self, config: GeneratorConfig) -> Map:
        grid = Map(config.width, config.height)
        rand = Randomizer(config.seed)

        for strategy in self.strategies:
            count = config.obstacle_counts.get(strategy.name, 0)
            for _ in range(count):
                strategy.apply(grid, rand, config)

        return grid
