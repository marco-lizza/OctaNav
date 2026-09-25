"""
Grid rendering canvas module for the interactive GUI.

This module provides the GridCanvas class, a custom PyQt6 widget acting
as the main 'View' component in the MVC architecture. It handles the
actual drawing of the map, obstacles, areas, and paths based on visibility flags.
"""

from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.grid_analyzer import AnalysisResult
from navigator.path_engine import FreePathResult


class GridCanvas(QWidget):
    """
    Custom QWidget responsible solely for rendering the grid and overlays.

    This class represents the 'View' in the MVC pattern. It receives the full
    navigational state (domain data) upon initialization and uses internal
    boolean flags to determine which analytical layers (Context, Complement, Paths)
    should be rendered during a paint event.
    """

    def __init__(
        self,
        grid: Grid,
        origin: Coordinate,
        dest: Coordinate,
        paths: FreePathResult,
        analysis: AnalysisResult,
    ):
        """
        Initializes the GridCanvas with the required navigational data.

        Sets up the widget dimensions based on the grid size and configures
        default visibility flags (all set to False) and rendering colors.

        Args:
            grid (Grid): The map model containing spatial constraints.
            origin (Coordinate): The starting point of the navigation.
            dest (Coordinate): The target destination of the navigation.
            paths (FreePathResult): DTO containing Type 1 and Type 2 paths.
            analysis (AnalysisResult): DTO containing Context and Complement areas.
        """
        super().__init__()
        self.grid = grid
        self.origin = origin
        self.dest = dest
        self.paths = paths
        self.analysis = analysis

        self.cell_size = 15
        self.setFixedSize(
            self.grid.width * self.cell_size, self.grid.height * self.cell_size
        )

        # Visibility Flags (Controlled by the UI / Controller)
        self.show_context = False
        self.show_complement = False
        self.show_path_1 = False
        self.show_path_2 = False
        self.show_closure = False
        self.show_border = False

        # Colors
        self.color_obs = QColor(50, 50, 50)
        self.color_ctx = QColor("#50B9DB")
        self.color_comp = QColor("#DD8FD4")
        self.color_p1 = QColor("#DC9A00")
        self.color_p2 = QColor("#8052CF")
        self.color_org = QColor("#0000FF")
        self.color_dst = QColor("#FF0000")
        self.color_clo = QColor("#26DD29")
        self.color_bor = QColor("#A74224")

    def paintEvent(self, event):
        """
        Handles the Qt paint event to render the grid and active overlays.

        The rendering follows a strict Z-order (bottom to top):
        1. Base grid (traversable cells, obstacles) and area highlights.
        2. Path overlays (Type 1 or Type 2).
        3. Origin and Destination cells (always drawn on top to ensure visibility).

        Args:
            event: The QPaintEvent triggered by the Qt framework.
        """
        painter = QPainter(self)

        # 1. Base Grid & Areas
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                coord = Coordinate(x, y)

                # Default to white
                color = QColor(255, 255, 255)

                if not self.grid.is_traversable(x, y):
                    color = self.color_obs
                elif (
                    self.show_border
                    and self.analysis.border
                    and coord in self.analysis.border
                ):
                    color = self.color_bor
                elif self.show_closure and (
                    coord in self.analysis.context or coord in self.analysis.complement
                ):
                    color = self.color_clo
                elif self.show_context and coord in self.analysis.context:
                    color = self.color_ctx
                elif self.show_complement and coord in self.analysis.complement:
                    color = self.color_comp

                painter.fillRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    color,
                )
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

        # 2. Paths Overlays
        if self.show_path_1 and self.paths.type_1_path:
            self._draw_path(painter, self.paths.type_1_path, self.color_p1)

        if self.show_path_2 and self.paths.type_2_path:
            self._draw_path(painter, self.paths.type_2_path, self.color_p2)

        # 3. Always draw Origin and Destination on top
        painter.fillRect(
            self.origin.x * self.cell_size,
            self.origin.y * self.cell_size,
            self.cell_size,
            self.cell_size,
            self.color_org,
        )
        painter.fillRect(
            self.dest.x * self.cell_size,
            self.dest.y * self.cell_size,
            self.cell_size,
            self.cell_size,
            self.color_dst,
        )

    def _draw_path(self, painter: QPainter, path: list[Coordinate], color: QColor):
        """
        Internal helper to draw a sequence of path coordinates on the canvas.

        Args:
            painter (QPainter): The active QPainter instance used for drawing.
            path (list[Coordinate]): The sequence of cells making up the path.
            color (QColor): The color used to fill the path cells.
        """
        for coord in path:
            painter.fillRect(
                coord.x * self.cell_size,
                coord.y * self.cell_size,
                self.cell_size,
                self.cell_size,
                color,
            )
            painter.drawRect(
                coord.x * self.cell_size,
                coord.y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
