from abc import ABC, abstractmethod

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid


class IPathStrategy(ABC):
    """
    Abstract Base Class defining the contract for path calculation strategies.
    """

    @abstractmethod
    def compute(
        self, grid: Grid, origin: Coordinate, destination: Coordinate
    ) -> list[Coordinate] | None:
        """
        Computes a specific type of path between origin and destination.

        Args:
            grid (Grid): The map model.
            origin (Coordinate): The starting cell.
            destination (Coordinate): The ending cell.

        Returns:
            list[Coordinate] | None: The computed path, or None if blocked/invalid.
        """

    def _sign(self, value: int) -> int:
        """
        Mathematical helper to extract the direction sign.
        Returns 1 if positive, -1 if negative, 0 if zero.
        """
        return (value > 0) - (value < 0)
