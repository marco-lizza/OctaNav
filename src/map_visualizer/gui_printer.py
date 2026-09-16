import sys

from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QWidget

from map_generator.models.grid import Grid
from map_generator.ui.i_grid_printer import IGridPrinter


class GridWidget(QWidget):
    """
    A PyQt6 QWidget responsible for actually drawing the grid map.

    Attributes:
        grid (Grid): The grid data model to draw.
        cell_size (int): The rendering size of each cell in pixels.
    """

    def __init__(self, grid: Grid):
        """
        Initializes the widget, setting its dimensions based on the grid size.

        Args:
            grid (Grid): The grid data model.
        """
        super().__init__()
        self.grid = grid
        self.cell_size = 15  # Dimension in pixels for each cell

        # Set the window size based on grid dimensions and cell size
        window_width = self.grid.width * self.cell_size
        window_height = self.grid.height * self.cell_size
        self.resize(window_width, window_height)
        self.setWindowTitle("Map Generator - 8-Connected Gridmap")

    def paintEvent(self, event):
        """
        Handles the PyQt6 paint event, drawing the cells and their borders.
        Traversable cells are white, obstacles are dark gray.

        Args:
            event: The QPaintEvent triggered by the window system.
        """
        painter = QPainter(self)

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Choose color: White for traversable, Dark Gray for obstacle
                if self.grid.cells[x][y].is_traversable:
                    color = QColor(255, 255, 255)
                else:
                    color = QColor(50, 50, 50)

                # Draw the colored block
                painter.fillRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    color,
                )

                # Draw the cell border to make the grid visible
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )


class GuiPrinter(IGridPrinter):
    """
    Implementation of IGridPrinter that launches a PyQt6 Graphical User Interface
    to visualize the map.
    """

    def print_map(self, grid: Grid) -> None:
        """
        Initializes the PyQt6 application (if not already running) and displays
        the GridWidget window containing the map.

        Args:
            grid (Grid): The grid object to display in the GUI.
        """
        # Check if a QApplication instance already exists (needed for multiple runs)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        window = GridWidget(grid)
        window.show()
        app.exec()
