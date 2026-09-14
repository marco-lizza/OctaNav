from MapGenerator.Config.Config import GeneratorConfig
from MapGenerator.Generator import Generator
from MapGenerator.UI.ConsolePrinter import ConsolePrinter
from MapGenerator.UI.GuiPrinter import GuiPrinter


def main():
    config = GeneratorConfig(
        width=30,
        height=20,
        seed=41,  # Imposta un seed fisso per testing o None per casualità pura
        obstacle_counts={
            "Bar": 5,  # 5 ostacoli a sbarra
            "Enclosure": 2,  # 2 recinti chiusi
            "Random": 15,  # 15 celle sparse
        },
    )

    generator = Generator()
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
