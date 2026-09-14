from abc import ABC, abstractmethod

from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.utils.Randomizer import Randomizer


class ObstacleStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, grid: Grid, rand: Randomizer, config: GeneratorConfig):
        pass
