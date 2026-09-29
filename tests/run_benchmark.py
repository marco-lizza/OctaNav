"""
Entry point for the OctaNav algorithm Benchmarking suite.
"""

import sys
from pathlib import Path

# Automatically set the 'src' folder as the root for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from benchmark_config import BenchmarkSuiteConfig
from benchmark_runner import BenchmarkRunner
from benchmark_storage import BenchmarkStorage
from benchmark_visualizer import BenchmarkVisualizer


def choose_existing_file(storage: BenchmarkStorage) -> dict | None:
    """
    Searches for existing JSON benchmark files, lists them,
    and prompts the user to select one to load.

    Args:
        storage (BenchmarkStorage): The storage handler to search and load files.

    Returns:
        dict | None: The loaded benchmark data dictionary, or None if cancelled or no files exist.
    """
    # Find all JSON files and sort them (newest first due to the timestamp in the name)
    files = sorted(list(storage.output_dir.glob("*.json")), reverse=True)

    if not files:
        print("\n[!] No benchmark files found in the results directory.")
        return None

    print("\nAvailable benchmark files:")
    for i, file_path in enumerate(files):
        print(f"  [{i}] {file_path.name}")

    while True:
        choice = input(
            f"\nSelect the file number to load (0-{len(files) - 1}) or 'q' to quit: "
        ).strip()

        if choice.lower() == "q":
            return None

        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(files):
                selected_file = files[idx]
                print(f"\nLoading data from {selected_file.name}...")
                return storage.load_results(selected_file)

        print("Invalid choice, please try again.")


def main():
    """
    Main function to run the benchmark suite.
    It provides a CLI for the user to either run a new benchmark
    or load an existing one for visualization.
    """
    print("=" * 60)
    print("OCTANAV - BENCHMARKING AND ANALYSIS SUITE")
    print("=" * 60)

    storage = BenchmarkStorage()

    print("\nSelect an operation:")
    print("  [1] Run a NEW Benchmark (Intensive computation, saves results)")
    print("  [2] Load and analyze an EXISTING Benchmark (Only generates plots)")

    main_choice = input("\nChoice [1/2]: ").strip()

    raw_results = None

    if main_choice == "1":
        config = BenchmarkSuiteConfig()
        runner = BenchmarkRunner(config)

        raw_results = runner.run_suite()

        # Automatic saving
        saved_file = storage.save_results(raw_results)
        print(f"\n[INFO] Raw data successfully saved to: {saved_file}")

    elif main_choice == "2":
        raw_results = choose_existing_file(storage)
        if raw_results is None:
            print("Operation cancelled.")
            sys.exit(0)
    else:
        print("Unrecognized choice. Exiting.")
        sys.exit(1)

    # Regardless of how we obtained raw_results (computed or loaded), generate the plots
    print("\nGenerating plots. Please check the Matplotlib windows...")
    visualizer = BenchmarkVisualizer(raw_results)
    visualizer.generate_all_plots()


if __name__ == "__main__":
    main()
