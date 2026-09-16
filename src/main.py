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
            "Bar": 2,
            "Enclosure": 2,
            "Random": 2,
            "Diagonal": 2,
        },
    )

    generator = GridGenerator()
    mappa = generator.generate_map(config)

    print(f"Mappa generata (Larghezza: {mappa.width}, Altezza: {mappa.height}):\n")
    consoleOrGui = input(
        "Scegli se presentare la mappa graficamente o a linea di comando ( 0 linea di comando - 1 o altri grafica)"
    )
    if consoleOrGui == "0":
        printer = ConsolePrinter()
    else:
        printer = GuiPrinter()

    printer.print_map(mappa)


if __name__ == "__main__":
    main()
