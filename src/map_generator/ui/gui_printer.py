import sys

from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QWidget

from map_generator.models.grid import Grid
from map_generator.ui.i_grid_printer import IGridPrinter


class GridWidget(QWidget):
    def __init__(self, grid: Grid):
        super().__init__()
        self.grid = grid
        self.cell_size = 15  # Dimensione in pixel di ogni cella

        # Imposta la dimensione della finestra in base alla griglia
        window_width = self.grid.width * self.cell_size
        window_height = self.grid.height * self.cell_size
        self.resize(window_width, window_height)
        self.setWindowTitle("Map Generator - 8-Connected Gridmap")

    def paintEvent(self, event):
        painter = QPainter(self)

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Scegli il colore: Bianco per attraversabile, Grigio scuro/Nero per ostacolo
                if self.grid.cells[x][y].is_traversable:
                    color = QColor(255, 255, 255)
                else:
                    color = QColor(50, 50, 50)

                # Disegna il blocco colorato
                painter.fillRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    color,
                )

                # Disegna il bordo della cella per far vedere la griglia
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )


class GuiPrinter(IGridPrinter):
    def print_map(self, grid: Grid) -> None:
        # Verifica se esiste già un'applicazione PyQt (necessario se si lancia più volte)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        window = GridWidget(grid)
        window.show()
        app.exec()
