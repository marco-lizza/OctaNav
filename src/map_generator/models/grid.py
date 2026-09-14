from map_generator.models.coordinate import Coordinate
from map_generator.models.grid_cell import GridCell


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [
            [GridCell(Coordinate(x, y)) for y in range(height)] for x in range(width)
        ]

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set_obstacle(self, x: int, y: int):
        if self.is_valid_coordinate(x, y):
            self.cells[x][y].is_traversable = False
