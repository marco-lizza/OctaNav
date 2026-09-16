from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_visualizer.console_printer import ConsolePrinter
from map_visualizer.gui_printer import GuiPrinter


def main():
    """
    Main entry point for the Octanav map generator application.
    Configures the parameters, generates the grid, and prompts the user
    to select the preferred visualization mode (CLI or GUI).
    """
    config = GeneratorConfig(
        width=30,
        height=20,
        seed=41,
        obstacle_counts={
            "Bar": 0,
            "Enclosure": 0,
            "Random": 0,
            "Diagonal": 0,
            "Agglomerate": 20,
        },
    )

    generator = GridGenerator()
    mappa = generator.generate_map(config)

    print(f"Map generated (Width: {mappa.width}, Height: {mappa.height}):\n")

    # User input to select the display mode
    consoleOrGui = input("Select display mode [0: CLI, 1: GUI (default)]:")

    if consoleOrGui == "0":
        printer = ConsolePrinter()
    else:
        printer = GuiPrinter()

    printer.print_map(mappa)


if __name__ == "__main__":
    main()
