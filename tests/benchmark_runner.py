import math
import signal
import time
import tracemalloc

from benchmark_config import BenchmarkSuiteConfig

from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from navigator.navigator import Navigator


class BenchmarkTimeoutException(Exception):
    """Sollevata quando scade il timer SIGALRM."""


def timeout_handler(signum, frame):
    raise BenchmarkTimeoutException()


class BenchmarkRunner:
    def __init__(self, config: BenchmarkSuiteConfig):
        self.config = config

    def run_suite(self) -> dict:
        results_data = {
            "metadata": {"watchdog_timeout": self.config.timeout_seconds},
            "correctness": [],
            "performance": [],
        }

        print("=" * 60)
        print("STARTING BENCHMARK PIPELINE")
        print("=" * 60)

        try:
            for width, height in self.config.grid_sizes:
                print(f"\n--- GRID {width}x{height} ---")

                for topo in self.config.topologies:
                    current_obstacle_counts = topo.get_counts(width, height)
                    counts_repr = ", ".join(
                        f"{k}:{v}" for k, v in current_obstacle_counts.items()
                    )
                    print(f"\n>> Topology: {topo.name} [{counts_repr}]")

                    gen_cfg = GeneratorConfig(width, height, current_obstacle_counts)
                    generator = GridGenerator(gen_cfg)

                    for seed in self.config.seeds:
                        mappa = generator.generate_map(seed)
                        origin, dest = generator.generate_origin_and_destination(
                            mappa, seed + 1
                        )
                        nav = Navigator(mappa)

                        print(
                            f"  [Seed {seed}] O:({origin.x},{origin.y}) -> D:({dest.x},{dest.y})"
                        )

                        # --- Correctness Test ---
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(self.config.timeout_seconds)

                        try:
                            c_dir, _, _ = nav.get_path(
                                origin,
                                dest,
                                mappa,
                                use_heuristic=True,
                                use_sorting=True,
                            )
                            c_rev, _, _ = nav.get_path(
                                dest,
                                origin,
                                mappa,
                                use_heuristic=True,
                                use_sorting=True,
                            )

                            is_correct = (
                                math.isclose(c_dir, c_rev, rel_tol=1e-9)
                                if c_dir != math.inf
                                else (c_dir == c_rev)
                            )
                            status = "Passed" if is_correct else "Failed"
                            print(
                                f"    Correctness: {status} (Forward: {c_dir:.2f}, Backward: {c_rev:.2f})"
                            )
                        except BenchmarkTimeoutException:
                            print(
                                f"    Correctness: TIMEOUT ({self.config.timeout_seconds}s)"
                            )
                            is_correct = False
                            c_dir = -1
                            c_rev = -1
                        finally:
                            signal.alarm(0)

                        results_data["correctness"].append(
                            {
                                "grid_size": f"{width}x{height}",
                                "topology": topo.name,
                                "seed": seed,
                                "is_correct": is_correct,
                                "cost_dir": c_dir if c_dir != math.inf else -1,
                                "cost_rev": c_rev if c_rev != math.inf else -1,
                            }
                        )

                        for strat_name, flags in self.config.strategies.items():
                            print(
                                f"    Running {strat_name: <18} ... ",
                                end="",
                                flush=True,
                            )

                            signal.signal(signal.SIGALRM, timeout_handler)
                            signal.alarm(self.config.timeout_seconds)

                            # Avvia tracciamento memoria e tempo
                            tracemalloc.start()
                            start_time = time.perf_counter()
                            stats = {}
                            cost = -1
                            completed = False
                            peak_memory_kb = 0.0

                            try:
                                cost_val, _, stats = nav.get_path(
                                    origin, dest, mappa, **flags
                                )
                                elapsed = time.perf_counter() - start_time

                                # Rileva il picco di memoria allocato dal codice Python
                                _, peak_bytes = tracemalloc.get_traced_memory()
                                peak_memory_kb = peak_bytes / 1024.0

                                cost = cost_val if cost_val != math.inf else -1
                                completed = not stats.get("interrupted", False)
                            except BenchmarkTimeoutException:
                                elapsed = time.perf_counter() - start_time
                                _, peak_bytes = tracemalloc.get_traced_memory()
                                peak_memory_kb = peak_bytes / 1024.0
                                completed = False
                            finally:
                                tracemalloc.stop()
                                signal.alarm(0)

                            result_record = {
                                "grid_size": f"{width}x{height}",
                                "topology": topo.name,
                                "seed": seed,
                                "strategy": strat_name,
                                "time_seconds": round(elapsed, 4),
                                "peak_memory_kb": round(
                                    peak_memory_kb, 2
                                ),  # <--- NUOVO DATO SPAZIALE
                                "completed": completed,
                                "cost": cost,
                                "paths_found": stats.get("paths_found", 0),
                                "branches_cut": stats.get("condition_false", 0),
                            }
                            results_data["performance"].append(result_record)
        except KeyboardInterrupt:
            print(
                "\n[!] Benchmark interrotto manualmente (Ctrl+C). Salvataggio dei dati parziali..."
            )

        print("PROCESSING ENDED")
        return results_data
