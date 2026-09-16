from abc import ABC, abstractmethod

from map_generator.config.config import GeneratorConfig
from map_generator.models.grid import Grid
from map_generator.utils.grid_randomizer import GridRandomizer


class ObstacleStrategy(ABC):
    """
    Abstract base class for all obstacle generation strategies.

    Implements the Strategy Design Pattern to decouple the grid structure
    from the specific algorithms used to generate obstacles.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Gets the identifier name of the obstacle strategy.

        Returns:
            str: The name of the strategy (e.g., 'Random', 'Bar').
        """

    @abstractmethod
    def apply(self, grid: Grid, rand: GridRandomizer, config: GeneratorConfig):
        """
        Applies the specific obstacle generation logic to the provided grid.

        Args:
            grid (Grid): The grid object where the obstacles will be placed.
            rand (Randomizer): The random number generator wrapper for reproducible results.
            config (GeneratorConfig): The configuration settings for the generator.
        """
