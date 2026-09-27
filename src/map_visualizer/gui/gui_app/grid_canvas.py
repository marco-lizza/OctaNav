"""
Grid rendering canvas module for the interactive GUI.

This module provides the GridCanvas class, a custom PyQt6 widget acting
as the main 'View' component in the MVC architecture. It dynamically draws
the map, obstacles, areas, and POIs based on visibility flags.
"""

from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.gui.gui_printer_settings import GUIPrinterSettings


class GridCanvas(QWidget):
    """
    Custom QWidget responsible solely for rendering the grid and overlays.
    """

    def __init__(
        self,
        grid: Grid,
        settings: GUIPrinterSettings,
        areas: list[
            tuple[str, list[Coordinate], list[tuple[str, list[Coordinate], int]], int]
        ],
    ):
        """
        Initializes the GridCanvas with the required map and overlay data.

        Args:
            grid (Grid): The map model containing spatial constraints.
            settings (GUIPrinterSettings): Visual styling settings (colors).
            areas: The data structure containing all layers, POIs, and their IDs.
        """
        super().__init__()
        self.grid = grid
        self.settings = settings
        self.areas = areas

        self.cell_size = 15
        self.setFixedSize(
            self.grid.width * self.cell_size, self.grid.height * self.cell_size
        )

        # Dictionary to track which layers are currently visible.
        # Key: Layer name (str), Value: Visibility state (bool)
        self.layer_visibility: dict[str, bool] = {
            name: False for name, _, _, _ in self.areas
        }

    def paintEvent(self, event):
        """
        Handles the Qt paint event to render the grid and active overlays.
        """
        painter = QPainter(self)

        # Draw Base Grid
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                color = (
                    self.settings.empty_cell_color
                    if self.grid.is_traversable(x, y)
                    else self.settings.obstacle_color
                )
                self._paint_cell(painter, x, y, color)

        # Draw active Areas and their POIs (respecting Z-order in the list)
        for name, area_coords, poi_groups, area_id in self.areas:
            if not self.layer_visibility.get(name, False):
                continue

            # Fallback color if ID is missing from settings (Magenta for easy debugging)
            area_color = self.settings.area_styles.get(area_id, QColor(255, 0, 255))

            # Draw main area cells
            for coord in area_coords:
                if 0 <= coord.y < self.grid.height and 0 <= coord.x < self.grid.width:
                    self._paint_cell(painter, coord.x, coord.y, area_color)

            # Draw POI groups belonging to this area on top
            for _, poi_coords, poi_id in poi_groups:
                poi_color = self.settings.area_styles.get(poi_id, QColor(0, 255, 255))
                for poi_coord in poi_coords:
                    if (
                        0 <= poi_coord.y < self.grid.height
                        and 0 <= poi_coord.x < self.grid.width
                    ):
                        self._paint_cell(painter, poi_coord.x, poi_coord.y, poi_color)

    def _paint_cell(self, painter: QPainter, x: int, y: int, color: QColor) -> None:
        """
        Helper method to render a single square cell with a border.
        """
        painter.fillRect(
            x * self.cell_size,
            y * self.cell_size,
            self.cell_size,
            self.cell_size,
            color,
        )
        painter.setPen(QColor(200, 200, 200))  # Light gray border
        painter.drawRect(
            x * self.cell_size,
            y * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
