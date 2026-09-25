"""
Main window module for the interactive GUI.

This module provides the MainWindow class, which serves as the primary container
and 'Controller' in the MVC architecture, assembling the grid canvas and the
control panel, and handling user interactions to update the view dynamically.
"""

from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from map_visualizer.gui_app.grid_canvas import GridCanvas


class MainWindow(QMainWindow):
    """
    Main application window embedding the control panel and the grid canvas.

    This class acts as both a container and a Controller. It creates the sidebar
    with checkboxes to toggle analytical layers, connects the user interface
    signals to internal callbacks, and updates the state of the GridCanvas (View)
    accordingly.
    """

    def __init__(self, canvas: GridCanvas, dlib_display: str):
        """
        Initializes the main window and assembles the UI layout.

        Args:
            canvas (GridCanvas): The custom widget responsible for rendering the map.
            dlib_display (str): A formatted string of the theoretical free distance
                to be displayed in the statistics section of the sidebar.
        """
        super().__init__()
        self.setWindowTitle("OctaNav - Interactive Dashboard")
        self.canvas = canvas

        # Main Widget and Layout setup
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Control Panel (Sidebar)
        sidebar = QVBoxLayout()

        # Stats Label
        stats = QLabel(f"<b>Theoretical dlib:</b> {dlib_display}")
        sidebar.addWidget(stats)

        sidebar.addSpacing(20)
        sidebar.addWidget(QLabel("<b>Toggle Layers:</b>"))

        # Checkboxes for toggling map layers
        self.cb_ctx = QCheckBox("Show Context (Blue)")
        self.cb_comp = QCheckBox("Show Complement (Pink)")
        self.cb_p1 = QCheckBox("Show Type 1 Path (Orange)")
        self.cb_p2 = QCheckBox("Show Type 2 Path (Purple)")
        self.cb_clo = QCheckBox("Show closure (Green)")

        # Connect Qt signals to update canvas callbacks
        self.cb_ctx.stateChanged.connect(self._toggle_context)
        self.cb_comp.stateChanged.connect(self._toggle_complement)
        self.cb_p1.stateChanged.connect(self._toggle_p1)
        self.cb_p2.stateChanged.connect(self._toggle_p2)
        self.cb_clo.stateChanged.connect(self._toggle_clo)

        sidebar.addWidget(self.cb_ctx)
        sidebar.addWidget(self.cb_comp)
        sidebar.addWidget(self.cb_p1)
        sidebar.addWidget(self.cb_p2)
        sidebar.addWidget(self.cb_clo)
        sidebar.addStretch()  # Push all sidebar elements to the top

        # Assemble Window
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.canvas)

    # Callbacks to update the canvas state and force a repaint

    def _toggle_context(self, state: int) -> None:
        """
        Callback triggered when the Context checkbox state changes.

        Args:
            state (int): The current state of the checkbox (0 for unchecked).
        """
        self.canvas.show_context = bool(state)
        self.canvas.update()

    def _toggle_complement(self, state: int) -> None:
        """
        Callback triggered when the Complement checkbox state changes.

        Args:
            state (int): The current state of the checkbox.
        """
        self.canvas.show_complement = bool(state)
        self.canvas.update()

    def _toggle_p1(self, state: int) -> None:
        """
        Callback triggered when the Type 1 Path checkbox state changes.

        Args:
            state (int): The current state of the checkbox.
        """
        self.canvas.show_path_1 = bool(state)
        self.canvas.update()

    def _toggle_p2(self, state: int) -> None:
        """
        Callback triggered when the Type 2 Path checkbox state changes.

        Args:
            state (int): The current state of the checkbox.
        """
        self.canvas.show_path_2 = bool(state)
        self.canvas.update()

    def _toggle_clo(self, state: int) -> None:
        """
        Callback triggered when the Closure checkbox state changes.

        Args:
            state (int): The current state of the checkbox.
        """
        self.canvas.show_closure = bool(state)
        self.canvas.update()
