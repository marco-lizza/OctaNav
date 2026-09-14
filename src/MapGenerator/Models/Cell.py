from dataclasses import dataclass

from MapGenerator.Models.Coordinate import Coordinate


@dataclass
class Cell:
    position: Coordinate
    is_traversable: bool = True
