"""
JSON implementation of the map storage strategy.

Handles serialization and deserialization of Grid models into JSON files,
automatically computing structural metadata such as obstacle percentages.
"""

import json
from pathlib import Path

from map_generator.models.grid import Grid
from map_storage.i_map_storage import IMapStorage


class JsonStorage(IMapStorage):
    """
    Handles saving and loading Grid objects using the JSON format.
    Automatically calculates and stores metadata such as obstacle percentage.
    """

    def save(self, grid: Grid, filepath: str) -> None:
        """
        Serializes the grid obstacles and computes metadata into a JSON file.

        Args:
            grid (Grid): The map model to serialize.
            filepath (str): The destination JSON file path.
        """
        obstacles = []
        for x in range(grid.width):
            for y in range(grid.height):
                if not grid.is_traversable(x, y):
                    obstacles.append({"x": x, "y": y})

        total_cells = grid.width * grid.height
        obstacle_count = len(obstacles)
        percentage = (
            round((obstacle_count / total_cells) * 100, 2) if total_cells else 0
        )

        data = {
            "metadata": {
                "width": grid.width,
                "height": grid.height,
                "total_cells": total_cells,
                "obstacle_count": obstacle_count,
                "obstacle_percentage": percentage,
            },
            "obstacles": obstacles,
        }

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load(self, filepath: str) -> Grid:
        """
        Deserializes a JSON file to reconstruct a Grid object.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            Grid: The fully reconstructed Grid instance.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        width = data["metadata"]["width"]
        height = data["metadata"]["height"]

        # Create an empty grid using the saved dimensions
        grid = Grid(width, height)

        # Repopulate obstacles using the provided Grid method
        for obs in data["obstacles"]:
            x, y = obs["x"], obs["y"]
            grid.set_obstacle(x, y)

        return grid
