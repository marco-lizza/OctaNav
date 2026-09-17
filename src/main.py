from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_generator.models.coordinate import Coordinate
from map_visualizer.console_printer import ConsolePrinter
from map_visualizer.gui_printer import GuiPrinter
from navigator.navigator import Navigator


def main():
    """
    Main entry point for the Octanav map generator application.
    Configures the parameters, generates the grid, analyzes paths,
    and prompts the user to select the preferred visualization mode.
    """
    config = GeneratorConfig(
        width=5,
        height=5,
        seed=41,
        obstacle_counts={
            "Bar": 0,
            "Enclosure": 0,
            "Random": 0,
            "Diagonal": 0,
            "Agglomerate": 3,
        },
    )

    # Generation
    generator = GridGenerator()
    mappa = generator.generate_map(config)

    # Navigation Setup
    nav = Navigator(mappa)

    # Choose two arbitrary coordinates for testing (ensure they are within boundaries)
    origin = Coordinate(0, 0)
    destination = Coordinate(3, 4)

    # Pathfinding & Analysis (Task 2)
    path_result = nav.get_paths_and_distance(origin, destination)
    analysis_result = nav.analyze_context(origin)

    dlib_display = (
        f"{path_result.dlib:.2f}"
        if path_result.dlib is not None
        else "N.A. (No free path exists)"
    )

    # Print the analytical report to the terminal
    print(f"\n--- Map generated (Width: {mappa.width}, Height: {mappa.height}) ---")
    print(f"Origin: {origin}, Destination: {destination}")
    print(f"Theoretical Free Distance (dlib): {dlib_display}")
    print(f"Type 1 Path: {'Found' if path_result.type_1_path else 'Blocked / N.A.'}")
    print(f"Type 2 Path: {'Found' if path_result.type_2_path else 'Blocked / N.A.'}")
    print(f"Context size: {len(analysis_result.context)} cells")
    print(f"Complement size: {len(analysis_result.complement)} cells")
    print("-" * 40 + "\n")

    # Display
    consoleOrGui = input("Select display mode [0: CLI, 1: GUI (default)]:")

    if consoleOrGui == "0":
        printer = ConsolePrinter()
    else:
        printer = GuiPrinter()

    # TODO: Update the printer to accept analysis_result, paths, and origin/destination!
    printer.print_map(mappa)


if __name__ == "__main__":
    main()
