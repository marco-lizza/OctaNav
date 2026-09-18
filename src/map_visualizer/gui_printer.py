"""
Graphical User Interface (GUI) visualization strategy module.

This module provides the GuiPrinter class, which implements the IGridPrinter
interface using the PyQt6 framework. It launches an interactive dashboard
allowing users to toggle various navigational layers on and off.
"""

import sys

from PyQt6.QtWidgets import QApplication

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid

# Import the MVC components for the interactive dashboard
from map_visualizer.gui_app.grid_canvas import GridCanvas
from map_visualizer.gui_app.main_window import MainWindow
from map_visualizer.i_grid_printer import IGridPrinter
from navigator.grid_analyzer import AnalysisResult
from navigator.path_engine import FreePathResult


class GuiPrinter(IGridPrinter):
    """
    Implementation of IGridPrinter that launches an interactive PyQt6 Dashboard.

    This class acts as a bridge between the core application logic and the
    Model-View-Controller (MVC) components of the GUI (`MainWindow` and `GridCanvas`).
    It manages the lifecycle of the `QApplication` and injects the domain data
    into the graphical views.
    """

    def _ensure_app(self) -> QApplication:
        """
        Ensures that a valid QApplication instance exists before creating widgets.

        PyQt6 requires exactly one QApplication instance per process. This internal
        helper retrieves the existing instance or creates a new one if it does
        not exist, preventing 'Must construct a QApplication' lifecycle errors.

        Returns:
            QApplication: The active PyQt application instance.
        """
        app = QApplication.instance()
        if isinstance(app, QApplication):
            return app
        return QApplication(sys.argv)

    def print_map(self, grid: Grid) -> None:
        """
        Renders the base grid in the interactive dashboard without overlays.

        Since the GUI is designed to expect navigational data, this method
        provides empty dummy data (null paths and empty sets) as a fallback,
        allowing the user to inspect the generated obstacles.

        Args:
            grid (Grid): The map model to display.
        """
        app = self._ensure_app()

        # Fallback to an empty dashboard if only the map is requested
        empty_paths = FreePathResult(dlib=None, type_1_path=None, type_2_path=None)
        empty_analysis = AnalysisResult(context=set(), complement=set())

        canvas = GridCanvas(
            grid, Coordinate(0, 0), Coordinate(0, 0), empty_paths, empty_analysis
        )
        window = MainWindow(canvas, "N.A.")
        window.show()
        app.exec()

    def print_analysis(
        self,
        grid: Grid,
        origin: Coordinate,
        dest: Coordinate,
        analysis: AnalysisResult,
        paths: FreePathResult,
    ) -> None:
        """
        Launches the interactive MVC dashboard for full navigation analysis.

        Assembles the canvas and the main window, injecting the computed
        domain data. It then starts the Qt event loop, pausing the main Python
        execution until the user closes the dashboard window.

        Args:
            grid (Grid): The map model.
            origin (Coordinate): The starting cell.
            dest (Coordinate): The destination cell.
            analysis (AnalysisResult): Context and Complement data.
            paths (FreePathResult): Type 1 and Type 2 paths data.
        """
        app = self._ensure_app()

        dlib_display = f"{paths.dlib:.2f}" if paths.dlib is not None else "N.A."

        # Assemble MVC components
        canvas = GridCanvas(grid, origin, dest, paths, analysis)
        window = MainWindow(canvas, dlib_display)

        window.show()
        app.exec()
