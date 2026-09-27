from dataclasses import dataclass

from map_visualizer.i_grid_printer import BasePrinterSettings


@dataclass
class CLIPrinterSettings(BasePrinterSettings):
    """
    Settings specifically for the Console/CLI printer.

    Attributes:
        area_styles (dict[int, str]): Inherited from BasePrinterSettings. Maps
            an area ID (int) to a string/character (e.g., 1 -> "C ", 2 -> "K ").
        empty_cell_char (str): Character representing traversable cells.
        obstacle_char (str): Character representing obstacles.
    """

    empty_cell_char: str = "."
    obstacle_char: str = "█"
