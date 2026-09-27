"""
Main window module for the interactive GUI.
"""

from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from map_visualizer.gui.gui_app.grid_canvas import GridCanvas


class MainWindow(QMainWindow):
    """
    Main application window embedding the control panel and the grid canvas.
    """

    def __init__(self, canvas: GridCanvas, title_info: str):
        """
        Initializes the main window and dynamically builds the UI layout.

        Args:
            canvas (GridCanvas): The custom widget responsible for rendering the map.
            title_info (str): Additional information to display in the UI (e.g., stats).
        """
        super().__init__()
        self.setWindowTitle("OctaNav - Interactive Dashboard")
        self.canvas = canvas

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        sidebar = QVBoxLayout()

        # Stats Label
        stats = QLabel(f"<b>Info:</b> {title_info}")
        sidebar.addWidget(stats)
        sidebar.addSpacing(20)
        sidebar.addWidget(QLabel("<b>Toggle Layers:</b>"))

        # Dynamically generate checkboxes based on the data layers provided
        for layer_name, _, _, _ in self.canvas.areas:
            cb = QCheckBox(f"Show {layer_name}")
            # Use a lambda with a default argument to avoid late-binding closure issues
            cb.stateChanged.connect(
                lambda state, name=layer_name: self._toggle_layer(name, state)
            )
            sidebar.addWidget(cb)

        sidebar.addStretch()  # Push everything to the top

        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.canvas)

    def _toggle_layer(self, layer_name: str, state: int) -> None:
        """
        Generic callback triggered when any dynamically generated checkbox is toggled.

        Args:
            layer_name (str): The name of the layer to toggle.
            state (int): The current state of the Qt checkbox.
        """
        self.canvas.layer_visibility[layer_name] = bool(state)
        self.canvas.update()  # Force a repaint of the canvas
