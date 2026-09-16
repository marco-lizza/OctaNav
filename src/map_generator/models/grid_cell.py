from dataclasses import dataclass

from map_generator.models.coordinate import Coordinate


@dataclass
class GridCell:
    """
    Represents a single cell within the grid map.

    Attributes:
        position (Coordinate): The exact (x, y) spatial coordinates of the cell.
        is_traversable (bool): Flag indicating if the cell can be walked on (True)
            or if it acts as an obstacle (False). Defaults to True.
    """

    position: Coordinate
    is_traversable: bool = True
