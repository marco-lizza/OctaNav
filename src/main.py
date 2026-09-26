from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_generator.models.coordinate import Coordinate
from map_storage.storage_facade import StorageFacade
from map_visualizer.console_printer import ConsolePrinter
from map_visualizer.gui_printer import GuiPrinter
from navigator.navigator import Navigator


def main():
    storage = StorageFacade()
    config = GeneratorConfig(
        width=20,
        height=20,
        seed=42,
        obstacle_counts={
            "Bar": 5,
            "Enclosure": 1,
            "Random": 5,
            "Diagonal": 5,
            "Agglomerate": 5,
        },
    )

    loadOrGenerate = input(
        "Load last, generate one or load master_test [0: Load last, 1: Generate, 2:Load master_test] (Default)"
    )

    origin = Coordinate(0, 0)
    destination = Coordinate(15, 12)

    if loadOrGenerate == "1":
        # Generation
        generator = GridGenerator()
        mappa = generator.generate_map(config)
        storage.save_map(mappa, "data/last_generated_map.json")
    elif loadOrGenerate == "0":
        mappa = storage.load_map("data/last_generated_map.json")
    else:
        mappa = storage.load_map("data/master_test.json")
        origin = Coordinate(6, 4)
        destination = Coordinate(19, 8)

    # Navigation Setup
    if mappa != None:
        nav = Navigator(mappa)

        # Pathfinding & Analysis
        path_result = nav.get_paths_and_distance(origin, destination)
        analysis_result = nav.analyze_context(origin)
        path_cammino_min = nav.get_path(origin, destination, mappa)

        print(nav.get_path_from_landmarks(path_cammino_min[1]))

        path_cammino_min = nav.get_path(destination, origin, mappa)
        print(path_cammino_min)

        # Display
        consoleOrGui = input("Select display mode [0: CLI, 1: GUI (default)]:")

        if consoleOrGui == "0":
            printer = ConsolePrinter()
        else:
            printer = GuiPrinter()

        printer.print_analysis(mappa, origin, destination, analysis_result, path_result)


if __name__ == "__main__":
    main()
