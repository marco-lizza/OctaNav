"""
Storage Facade module.

Provides a unified, high-level interface to save and load maps
without exposing the underlying serialization strategies.
"""

from pathlib import Path

from map_generator.models.grid import Grid
from map_storage.i_map_storage import IMapStorage
from map_storage.storages.json_storage import JsonStorage


class StorageFacade:
    """
    Facade class for the map storage module.

    Automatically routes save/load requests to the correct strategy
    based on the file extension (e.g., '.json').
    """

    def __init__(self):
        """
        Initializes the facade and registers the available storage strategies.
        """
        self._strategies: dict[str, IMapStorage] = {
            ".json": JsonStorage(),
            # Future extensions go here (e.g., ".csv": CsvStorage())
        }

    def _get_strategy(self, filepath: str) -> IMapStorage:
        """
        Internal helper to resolve the correct strategy from the file extension.

        Args:
            filepath (str): The file path being processed.

        Returns:
            IMapStorage: The resolved strategy for the format.

        Raises:
            ValueError: If the file extension is not supported.
        """
        ext = Path(filepath).suffix.lower()
        if ext not in self._strategies:
            raise ValueError(
                f"Unsupported file format: '{ext}'. "
                f"Supported formats: {list(self._strategies.keys())}"
            )
        return self._strategies[ext]

    def save_map(self, grid: Grid, filepath: str) -> None:
        """
        Saves the grid to the specified file path.

        Args:
            grid (Grid): The map model to save.
            filepath (str): The destination path (e.g., 'data/map1.json').
        """
        strategy = self._get_strategy(filepath)
        strategy.save(grid, filepath)
        print(f"Map successfully saved to {filepath}")

    def load_map(self, filepath: str) -> Grid | None:
        """
        Loads a grid from the specified file path.

        Args:
            filepath (str): The source file path.

        Returns:
            Grid: The fully reconstructed map model.
        """
        try:
            strategy = self._get_strategy(filepath)
            grid = strategy.load(filepath)
            print(f"Map successfully loaded from {filepath}")
        except FileNotFoundError:
            print(f"Error during loading from {filepath} - file not found")
            return None
        return grid
