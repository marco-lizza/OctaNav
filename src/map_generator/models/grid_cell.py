from dataclasses import dataclass

from map_generator.models.coordinate import Coordinate


@dataclass
class GridCell:
    position: Coordinate
    is_traversable: bool = True
