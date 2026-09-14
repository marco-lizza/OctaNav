from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Models.Map import Map
from MapGenerator.Obstacles.ObstacleStrategy import ObstacleStrategy
from MapGenerator.Utils.Randomizer import Randomizer


class BarObstacle(ObstacleStrategy):
    @property
    def name(self) -> str:
        return "Bar"

    def apply(self, map: Map, rand: Randomizer, config: GeneratorConfig):
        x = rand.next_int(0, map.width)
        y = rand.next_int(0, map.height)
        length = rand.next_int(3, 15)
        is_horizontal = rand.next_bool()

        for i in range(length):
            if is_horizontal:
                map.set_obstacle(x + i, y)
            else:
                map.set_obstacle(x, y + i)
