import json
from datetime import datetime
from pathlib import Path


class BenchmarkStorage:
    def __init__(self, output_dir: str = "tests/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_results(self, results_data: dict, prefix: str = "benchmark"):
        """Salva i dati in un file JSON con timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{prefix}_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=4)

        print(f"[Storage] RESULTS saved in: {filename}")
        return filename

    def load_results(self, filepath: str | Path) -> dict:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
