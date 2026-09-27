"""
Settings module for the GUI visualization strategy.
"""

from dataclasses import dataclass, field

from PyQt6.QtGui import QColor

from map_visualizer.util.base_printer_settings import BasePrinterSettings


@dataclass
class GUIPrinterSettings(BasePrinterSettings):
    """
    Settings specifically for the GUI printer.

    Attributes:
        area_styles (dict[int, QColor]): Inherited from BasePrinterSettings. Maps
            an area or POI ID (int) to a specific PyQt6 QColor.
        empty_cell_color (QColor): Color representing traversable cells.
        obstacle_color (QColor): Color representing obstacles.
    """

    empty_cell_color: QColor = field(default_factory=lambda: QColor(255, 255, 255))
    obstacle_color: QColor = field(default_factory=lambda: QColor(50, 50, 50))
