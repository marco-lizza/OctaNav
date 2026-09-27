"""
Graphical User Interface (GUI) visualization strategy module.

This module provides the GuiPrinter class, which implements the IGridPrinter
interface. It delegates the creation of the interactive dashboard to the
InteractiveGuiFacade.
"""

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.gui.gui_app.gui_facade import InteractiveGuiFacade
from map_visualizer.gui.gui_printer_settings import GUIPrinterSettings
from map_visualizer.i_grid_printer import IGridPrinter


class GuiPrinter(IGridPrinter):
    """
    Implementation of IGridPrinter that launches an interactive PyQt6 Dashboard.

    This class acts as the concrete strategy for GUI rendering. It relies on the
    InteractiveGuiFacade to handle Qt-specific initialization and MVC assembly.
    """

    def __init__(self, grid: Grid, settings: GUIPrinterSettings) -> None:
        """
        Initializes the GUI printer with the map and the visual settings.
        """
        super().__init__(grid, settings)
        self.settings: GUIPrinterSettings = settings
        self.facade = InteractiveGuiFacade()

    def print_map(self) -> None:
        """
        Renders the base grid in the interactive dashboard without any overlays.
        """
        # Pass an empty list of areas for a map-only view
        self.facade.launch(
            grid=self.grid, settings=self.settings, areas=[], title_info="Map Only Mode"
        )

    def print_areas(
        self,
        areas: list[
            tuple[str, list[Coordinate], list[tuple[str, list[Coordinate], int]], int]
        ],
    ) -> None:
        """
        Launches the GUI dashboard with dynamic layers and POIs.

        Args:
            areas: List of tuples containing layer data. Each element defines a
                   layer name, main coordinates, POI groups, and style ID.
        """
        self.facade.launch(
            grid=self.grid,
            settings=self.settings,
            areas=areas,
            title_info=f"{len(areas)} Layers Loaded",
        )
