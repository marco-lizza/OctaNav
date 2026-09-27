"""
Interactive GUI Facade module.

This module provides the InteractiveGuiFacade class, which serves as a simplified
entry point for bootstrapping and launching the PyQt6 interactive dashboard,
hiding the underlying complexity of the MVC assembly and Qt lifecycle management.
"""

import sys

from PyQt6.QtWidgets import QApplication

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from map_visualizer.gui.gui_app.grid_canvas import GridCanvas
from map_visualizer.gui.gui_app.main_window import MainWindow
from map_visualizer.gui.gui_printer_settings import GUIPrinterSettings


class InteractiveGuiFacade:
    """
    Facade providing a unified entry point to launch the interactive UI dashboard.

    This class encapsulates the boilerplate code required to safely initialize
    the Qt environment, instantiate the Model-View-Controller (MVC) components
    (`GridCanvas` and `MainWindow`), wire them together with the generic map data,
    and start the application's main event loop.
    """

    def launch(
        self,
        grid: Grid,
        settings: GUIPrinterSettings,
        areas: list[
            tuple[str, list[Coordinate], list[tuple[str, list[Coordinate], int]], int]
        ],
        title_info: str = "OctaNav Dashboard",
    ) -> None:
        """
        Initializes the PyQt application, assembles components, and starts the event loop.

        This method ensures a valid QApplication instance exists, creates the canvas
        (View) and the main window (Controller), and passes the dynamic layers (Data)
        to them. Execution of the calling script will block at `q_app.exec()` until
        the user closes the dashboard window.

        Args:
            grid (Grid): The map model containing spatial constraints and obstacles.
            settings (GUIPrinterSettings): Visual styling settings (colors).
            areas: List of tuples containing dynamic layer data, POIs, and their IDs.
            title_info (str): A string to display in the UI's statistics section.
        """
        app = QApplication.instance()
        if isinstance(app, QApplication):
            q_app = app
        else:
            q_app = QApplication(sys.argv)

        # Assemble the UI components (MVC injection)
        canvas = GridCanvas(grid, settings, areas)
        window = MainWindow(canvas, title_info)

        window.show()
        q_app.exec()
