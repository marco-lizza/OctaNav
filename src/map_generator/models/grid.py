from map_generator.models.coordinate import Coordinate
from map_generator.models.grid_cell import GridCell


class Grid:
    """
    Represents the 2D grid map comprising traversable and non-traversable cells.

    This class handles the spatial data and ensures boundary safety for
    any operation performed on the grid.

    Attributes:
        width (int): The total number of columns in the grid.
        height (int): The total number of rows in the grid.
        cells (list[list[GridCell]]): A 2D matrix (list of lists) storing the GridCell objects.
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the grid with the specified dimensions, filling it with
        default traversable cells.

        Args:
            width (int): The total width of the grid.
            height (int): The total height of the grid.
        """
        self.width = width
        self.height = height
        self.cells = [
            [GridCell(Coordinate(x, y)) for y in range(height)] for x in range(width)
        ]

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """
        Checks whether the given (x, y) coordinates fall within the grid boundaries.

        Args:
            x (int): The X-axis coordinate to check.
            y (int): The Y-axis coordinate to check.

        Returns:
            bool: True if the coordinates are inside the grid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def set_obstacle(self, x: int, y: int):
        """
        Marks a specific cell as a non-traversable obstacle.
        Safely ignores out-of-bounds coordinates.

        Args:
            x (int): The X-axis coordinate of the cell.
            y (int): The Y-axis coordinate of the cell.
        """
        if self.is_valid_coordinate(x, y):
            self.cells[x][y].is_traversable = False
