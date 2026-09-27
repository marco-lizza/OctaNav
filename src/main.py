import math
import time

from PyQt6.QtGui import QColor

from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from map_generator.models.coordinate import Coordinate
from map_storage.storage_facade import StorageFacade
from map_visualizer.cli.cli_printer_settings import CLIPrinterSettings
from map_visualizer.cli.console_printer import ConsolePrinter
from map_visualizer.gui.gui_printer import GuiPrinter
from map_visualizer.gui.gui_printer_settings import GUIPrinterSettings
from navigator.navigator import Navigator
from utils.execution_reporter import ExecutionReporter

WIDTH = 15
HEIGHT = 15

MAP_SEED = 42
ORIGIN_AND_DESTINATION_SEED = 48

BAR_OBSTACLE = 2
ENCLOSURE_OBSTACLE = 1
RANDOM_OBSTACLE = 2
DIAGONAL_OBSTACLE = 2
AGGLOMERATE_OBSTACLE = 2

# CLI Configuration (Characters)
CLI_SETTINGS = {1: "P ", 10: "O ", 11: "D ", 12: "L "}

# GUI Configuration (Colors)
GUI_SETTINGS = {
    1: QColor("#DC9A00"),  # Path (Orange)
    10: QColor("#0000FF"),  # Origin (Blue)
    11: QColor("#FF0000"),  # Destination (Red)
    12: QColor("#26DD29"),  # Landmark (Green)
}

USE_HEURISTIC = False
USE_SORTING = False

# Togle this flag to switch between Console and Dashboard rendering
CLI = False
# Togle this to switch between Test and Normal mode
TEST = True
# Togle to load a map from a file or generate one
LOAD = False
# Togle to load master map or the last
LOAD_MASTER = False

MASTER_MAP_FILE = "data/master_test.json"
LAST_MAP_FILE = "data/last_generated_map.json"


def main():
    storage = StorageFacade()
    config = GeneratorConfig(
        width=WIDTH,
        height=HEIGHT,
        obstacle_counts={
            "Bar": BAR_OBSTACLE,
            "Enclosure": ENCLOSURE_OBSTACLE,
            "Random": RANDOM_OBSTACLE,
            "Diagonal": DIAGONAL_OBSTACLE,
            "Agglomerate": AGGLOMERATE_OBSTACLE,
        },
    )
    generator = GridGenerator(config)

    if LOAD:
        if LOAD_MASTER:
            mappa = storage.load_map(MASTER_MAP_FILE)
            origin = Coordinate(6, 4)
            destination = Coordinate(19, 8)
        else:
            mappa = storage.load_map(LAST_MAP_FILE)
            if mappa is not None:
                origin, destination = generator.generate_origin_and_destination(
                    mappa, ORIGIN_AND_DESTINATION_SEED
                )
    else:
        # Generation
        mappa = generator.generate_map(MAP_SEED)
        storage.save_map(mappa, LAST_MAP_FILE)
        origin, destination = generator.generate_origin_and_destination(
            mappa, ORIGIN_AND_DESTINATION_SEED
        )

    # Navigation Setup
    if mappa is not None:
        nav = Navigator(mappa)
        areas_to_print = []

        print(
            "\nCalculation in progress... press Ctrl+C to stop and view the partial result."
        )

        start_time = time.perf_counter()
        path_min_cost, path_min_seq, path_stats = nav.get_path(
            origin, destination, mappa, USE_HEURISTIC, USE_SORTING
        )
        time_elapsed = time.perf_counter() - start_time

        path_found = path_min_cost != math.inf

        if not path_found:
            print("\nNo direct path found or interrupted too early!")
        else:
            print(f"\nLength of direct path min: {path_min_cost:.4f}")
            landmark_coords = [coord for coord, _ in path_min_seq]
            areas_to_print.append(
                (
                    "Direct path",
                    nav.get_path_from_landmarks(path_min_seq),
                    [
                        ("Landmark", landmark_coords, 12),
                        ("Origin", [origin], 10),
                        ("Destination", [destination], 11),
                    ],
                    1,
                )
            )

        if TEST:
            print("\nCalculation of reverse path in progress... press Ctrl+C to stop.")

            start_time_rev = time.perf_counter()
            reverse_path_min_cost, reverse_path_min_seq, reverse_stats = nav.get_path(
                destination, origin, mappa, USE_HEURISTIC, USE_SORTING
            )
            time_elapsed_rev = time.perf_counter() - start_time_rev

            reverse_path_found = reverse_path_min_cost != math.inf

            if not reverse_path_found:
                print("\nNo reverse path found or interrupted too early!")
            else:
                reverse_landmark_coords = [coord for coord, _ in reverse_path_min_seq]
                areas_to_print.append(
                    (
                        "Reverse path",
                        nav.get_path_from_landmarks(reverse_path_min_seq),
                        [
                            ("Landmark", reverse_landmark_coords, 12),
                            ("Origin", [destination], 10),
                            ("Destination", [origin], 11),
                        ],
                        1,
                    )
                )

        if (
            TEST
            and path_found
            and reverse_path_found
            and not path_stats.get("interrupted")
            and not reverse_stats.get("interrupted")
        ):
            print()
            if math.isclose(path_min_cost, reverse_path_min_cost, rel_tol=1e-9):
                print("TEST RESULT - CORRECT")
            else:
                print("TEST RESULT - WRONG")

        user_choice = input("Do you want to see the execution summary? (y/n): ")

        if user_choice.lower() in ["y", "yes", "s", "si"]:
            ExecutionReporter.print_report(
                width=WIDTH,
                height=HEIGHT,
                obstacle_counts=config.obstacle_counts,
                time_elapsed=time_elapsed,
                path_stats=path_stats,
                is_test=TEST,
                time_elapsed_rev=time_elapsed_rev if TEST else 0.0,
                reverse_stats=reverse_stats if TEST else None,
            )

        # --- RENDERING ---
        if areas_to_print:
            if CLI:
                cli_settings = CLIPrinterSettings(area_styles=CLI_SETTINGS)
                printer = ConsolePrinter(grid=mappa, settings=cli_settings)

                printer.print_map()
                printer.print_areas(areas_to_print)
            else:
                gui_settings = GUIPrinterSettings(area_styles=GUI_SETTINGS)
                printer = GuiPrinter(grid=mappa, settings=gui_settings)

                printer.print_areas(areas_to_print)
        else:
            print(
                "[INFO] Skipping map rendering because no valid paths were found to display."
            )


if __name__ == "__main__":
    main()
