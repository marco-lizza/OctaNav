from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_generator.models.coordinate import Coordinate
from map_visualizer.console_printer import ConsolePrinter
from map_visualizer.gui_printer import GuiPrinter
from navigator.navigator import Navigator


def main():
    config = GeneratorConfig(
        width=15,
        height=15,
        seed=41,
        obstacle_counts={
            "Bar": 0,
            "Enclosure": 0,
            "Random": 0,
            "Diagonal": 0,
            "Agglomerate": 5,
        },
    )

    # Generation
    generator = GridGenerator()
    mappa = generator.generate_map(config)

    # Navigation Setup
    nav = Navigator(mappa)
    origin = Coordinate(5, 2)
    destination = Coordinate(10, 10)

    # Pathfinding & Analysis
    path_result = nav.get_paths_and_distance(origin, destination)
    analysis_result = nav.analyze_context(origin)

    dlib_display = f"{path_result.dlib:.2f}" if path_result.dlib is not None else "N.A."

    # Report
    print(f"\n--- Map generated ({mappa.width}x{mappa.height}) ---")
    print(f"Origin: {origin}, Destination: {destination}")
    print(f"dlib: {dlib_display}")
    print(
        f"Context: {len(analysis_result.context)} cells, Complement: {len(analysis_result.complement)} cells"
    )

    # Display
    consoleOrGui = input("Select display mode [0: CLI, 1: GUI (default)]:")

    if consoleOrGui == "0":
        printer = ConsolePrinter()
    else:
        printer = GuiPrinter()

    printer.print_analysis(mappa, origin, destination, analysis_result, path_result)


if __name__ == "__main__":
    main()
