from abc import ABC, abstractmethod

from map_generator.models.grid import Grid


class IGridPrinter(ABC):
    """
    Abstract base class defining the contract for grid visualization strategies.

    Any class responsible for rendering the map (e.g., to the console,
    to an image, or via a GUI) must implement this interface.
    """

    @abstractmethod
    def print_map(self, grid: Grid) -> None:
        """
        Renders the provided grid.

        Args:
            grid (Grid): The grid object containing the spatial and obstacle data
                to be visualized.
        """
