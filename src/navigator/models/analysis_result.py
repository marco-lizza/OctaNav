from dataclasses import dataclass

from map_generator.models.coordinate import Coordinate


@dataclass
class AnalysisResult:
    """
    Data Transfer Object (DTO) containing the results of the grid analysis.

    Attributes:
        context (set[Coordinate]): Cells reachable from the origin via a Type 1 free path.
        complement (set[Coordinate]): Cells reachable from the origin ONLY via a Type 2 free path.
        border (dict[Coordinate, int]): Frontier cells belonging to the context and complement that are adjacent to the excluded cells.
        excluded (set[Coordinate]): Cells that are not included in either the context or the complement.
    """

    context: set[Coordinate]
    complement: set[Coordinate]
    border: dict[Coordinate, int]
    excluded: set[Coordinate]
