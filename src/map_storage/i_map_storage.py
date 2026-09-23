"""
Interface definition for map storage strategies.

This module provides the IMapStorage abstract base class, establishing
the contract for saving and loading Grid objects to and from various
file formats (e.g., JSON, CSV).
"""

from abc import ABC, abstractmethod

from map_generator.models.grid import Grid


class IMapStorage(ABC):
    """
    Abstract base class for map persistence strategies.
    """

    @abstractmethod
    def save(self, grid: Grid, filepath: str) -> None:
        """
        Serializes a Grid object and its metadata to a file.

        Args:
            grid (Grid): The map model to save.
            filepath (str): The destination path for the saved file.
        """

    @abstractmethod
    def load(self, filepath: str) -> Grid:
        """
        Deserializes a file into a Grid object.

        Args:
            filepath (str): The path to the file to be loaded.

        Returns:
            Grid: The reconstructed map model.
        """
