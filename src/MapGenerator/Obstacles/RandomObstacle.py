from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Models.Map import Map
from MapGenerator.Obstacles.ObstacleStrategy import ObstacleStrategy
from MapGenerator.Utils.Randomizer import Randomizer


class RandomObstacle(ObstacleStrategy):
    @property
    def name(self) -> str:
        return "Random"

    def apply(self, map: Map, rand: Randomizer, config: GeneratorConfig):
        x = rand.next_int(0, map.width)
        y = rand.next_int(0, map.height)
        map.set_obstacle(x, y)
