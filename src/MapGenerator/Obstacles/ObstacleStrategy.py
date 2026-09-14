from abc import ABC, abstractmethod

from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Models.Map import Map
from MapGenerator.Utils.Randomizer import Randomizer


class ObstacleStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, map: Map, rand: Randomizer, config: GeneratorConfig):
        pass
