from abc import ABC, abstractmethod

from map_generator.models.grid import Grid


class IGridPrinter(ABC):
    @abstractmethod
    def print_map(self, grid: Grid) -> None:
        """Metodo che deve essere implementato da tutti i printer."""
