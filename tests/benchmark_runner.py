import math
import signal
import time

from benchmark_config import BenchmarkSuiteConfig

from map_generator.config.config import GeneratorConfig
from map_generator.grid_generator import GridGenerator
from navigator.navigator import Navigator


def timeout_handler(signum, frame):
    raise KeyboardInterrupt()


class BenchmarkRunner:
    def __init__(self, config: BenchmarkSuiteConfig):
        self.config = config

    def run_suite(self) -> dict:
        results_data = {
            "metadata": {"timeout_seconds": self.config.timeout_seconds},
            "correctness": [],
            "performance": [],
        }

        print("=" * 60)
        print("STARTING BENCHMARK PIPELINE")
        print("=" * 60)

        for width, height in self.config.grid_sizes:
            print(f"\n--- GRID {width}x{height} ---")

            for topo in self.config.topologies:
                print(f"\n>> Topology: {topo.name}")

                gen_cfg = GeneratorConfig(width, height, topo.obstacle_counts)
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

                    print(f"--- Correctness Test ({topo.name}) ---")

                    max_timeout = max(self.config.timeout_seconds)
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(max_timeout)

                    try:
                        c_dir, _, _ = nav.get_path(
                            origin, dest, mappa, use_heuristic=True, use_sorting=True
                        )
                        c_rev, _, _ = nav.get_path(
                            dest, origin, mappa, use_heuristic=True, use_sorting=True
                        )

                        is_correct = (
                            math.isclose(c_dir, c_rev, rel_tol=1e-9)
                            if c_dir != math.inf
                            else (c_dir == c_rev)
                        )
                        status = "Passed" if is_correct else "Failed"
                        print(
                            f"Correctness result: {status} (Forward: {c_dir:.2f}, Backward: {c_rev:.2f})"
                        )
                    except KeyboardInterrupt:
                        print(f"TIMEOUT ({max_timeout}s)")
                        is_correct = None
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
                        sorted_timeouts = sorted(self.config.timeout_seconds)

                        for current_timeout in sorted_timeouts:
                            print(
                                f"    Running {strat_name: <18} (Timeout: {current_timeout}s) ... ",
                                end="",
                                flush=True,
                            )

                            signal.signal(signal.SIGALRM, timeout_handler)
                            signal.alarm(current_timeout)  # Usiamo il timeout corrente!

                            start_time = time.perf_counter()
                            try:
                                cost, _, stats = nav.get_path(
                                    origin, dest, mappa, **flags
                                )
                            finally:
                                signal.alarm(0)

                            elapsed = time.perf_counter() - start_time
                            interrupted = stats.get("interrupted", False)

                            # Creiamo il record del risultato
                            result_record = {
                                "grid_size": f"{width}x{height}",
                                "topology": topo.name,
                                "seed": seed,
                                "strategy": strat_name,
                                "timeout_limit": current_timeout,  # Salviamo il timeout usato
                                "time_seconds": elapsed,
                                "cost": cost if cost != math.inf else -1,
                                "paths_found": stats.get("paths_found", 0),
                                "branches_cut": stats.get("condition_false", 0),
                                "interrupted": interrupted,
                            }
                            results_data["performance"].append(result_record)

                            status_msg = "[TIMEOUT]" if interrupted else "[COMPLETED]"
                            print(
                                f"{status_msg} in {elapsed:.2f}s | Cost: {cost:.2f} | Branches cut: {stats.get('condition_false', 0)}"
                            )

                            if not interrupted:
                                current_idx = sorted_timeouts.index(current_timeout)
                                remaining_timeouts = sorted_timeouts[current_idx + 1 :]

                                if remaining_timeouts:
                                    print(
                                        f"      ↳ [SKIP] The algorithm ended with success. "
                                        f"Skip test with greater timeout - {remaining_timeouts}."
                                    )

                                    for t in remaining_timeouts:
                                        copied_record = dict(result_record)
                                        copied_record["timeout_limit"] = t
                                        results_data["performance"].append(
                                            copied_record
                                        )

                                break
        print("\n" + "=" * 60)
        print("PROCESSING ENDED")
        return results_data
