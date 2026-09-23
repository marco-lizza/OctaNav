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
from map_visualizer.gui_app.grid_canvas import GridCanvas
from map_visualizer.gui_app.main_window import MainWindow
from navigator.grid_analyzer import AnalysisResult
from navigator.path_engine import FreePathResult


class InteractiveGuiFacade:
    """
    Facade providing a unified entry point to launch the interactive UI dashboard.

    This class encapsulates the boilerplate code required to safely initialize
    the Qt environment, instantiate the Model-View-Controller (MVC) components
    (`GridCanvas` and `MainWindow`), wire them together with the domain data,
    and start the application's main event loop.
    """

    def launch(
        self,
        grid: Grid,
        origin: Coordinate,
        dest: Coordinate,
        paths: FreePathResult,
        analysis: AnalysisResult,
        dlib_display: str,
    ) -> None:
        """
        Initializes the PyQt application, assembles components, and starts the event loop.

        This method ensures a valid QApplication instance exists, creates the canvas
        (View) and the main window (Controller/View wrapper), and passes the
        navigational models (Data) to them. Execution of the calling script will
        block at `q_app.exec()` until the user closes the dashboard window.

        Args:
            grid (Grid): The map model containing spatial constraints and obstacles.
            origin (Coordinate): The starting cell for the navigation.
            dest (Coordinate): The target destination cell.
            paths (FreePathResult): DTO containing Type 1 and Type 2 paths.
            analysis (AnalysisResult): DTO containing Context and Complement areas.
            dlib_display (str): A pre-formatted string representing the theoretical
                free distance (e.g., "14.14" or "N.A.") to display in the UI.
        """
        app = QApplication.instance()
        if isinstance(app, QApplication):
            q_app = app
        else:
            q_app = QApplication(sys.argv)

        # Assemble the UI components (MVC injection)
        canvas = GridCanvas(grid, origin, dest, paths, analysis)
        window = MainWindow(canvas, dlib_display)

        window.show()
        q_app.exec()
