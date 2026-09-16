from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_generator.ui.console_printer import ConsolePrinter
from map_generator.ui.gui_printer import GuiPrinter


def main():
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
    consoleOrGui = input("Select display mode [0: CLI, 1: GUI (default)]:")
    if consoleOrGui == "0":
        printer = ConsolePrinter()
    else:
        printer = GuiPrinter()

    printer.print_map(mappa)


if __name__ == "__main__":
    main()
