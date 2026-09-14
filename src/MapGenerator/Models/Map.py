from MapGenerator.Models.Cell import Cell
from MapGenerator.Models.Coordinate import Coordinate


class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Inizializziamo la griglia come matrice [x][y] per mantenere la coerenza con le coordinate cartesiane
        self.cells = [
            [Cell(Coordinate(x, y)) for y in range(height)] for x in range(width)
        ]

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set_obstacle(self, x: int, y: int):
        if self.is_valid_coordinate(x, y):
            self.cells[x][y].is_traversable = False
