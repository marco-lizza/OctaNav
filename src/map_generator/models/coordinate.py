from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    """
    Represents a 2D spatial coordinate within the grid.

    Attributes:
        x (int): The X-axis coordinate (column index).
        y (int): The Y-axis coordinate (row index).
    """

    x: int
    y: int
