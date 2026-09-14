from abc import ABC, abstractmethod

from MapGenerator.Models.Map import Map


class IGridPrinter(ABC):
    @abstractmethod
    def print_map(self, map: Map) -> None:
        """Metodo che deve essere implementato da tutti i printer."""
