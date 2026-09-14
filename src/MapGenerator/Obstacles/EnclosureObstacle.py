from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Models.Map import Map
from MapGenerator.Obstacles.ObstacleStrategy import ObstacleStrategy
from MapGenerator.Utils.Randomizer import Randomizer


class EnclosureObstacle(ObstacleStrategy):
    @property
    def name(self) -> str:
        return "Enclosure"

    def apply(self, map: Map, rand: Randomizer, config: GeneratorConfig):
        w = rand.next_int(4, 12)
        h = rand.next_int(4, 12)

        # Ci assicuriamo di non sforare i bordi della mappa in fase di posizionamento
        start_x = rand.next_int(0, max(1, map.width - w))
        start_y = rand.next_int(0, max(1, map.height - h))

        # Disegna il perimetro
        for i in range(w):
            map.set_obstacle(start_x + i, start_y)  # Top
            map.set_obstacle(start_x + i, start_y + h - 1)  # Bottom
        for j in range(h):
            map.set_obstacle(start_x, start_y + j)  # Left
            map.set_obstacle(start_x + w - 1, start_y + j)  # Right
