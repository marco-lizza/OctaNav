import os

import matplotlib.pyplot as plt
import numpy as np


class BenchmarkVisualizer:
    """
    A class to visualize benchmark results for different pathfinding algorithms.
    It generates and saves various plots comparing performance, correctness,
    scalability, and efficiency.
    """

    def __init__(self, data: dict):
        """
        Initializes the visualizer with benchmark data.

        Args:
            data (dict): A dictionary containing 'performance' and 'correctness' data.
        """
        self.performance_data = data["performance"]
        self.correctness_data = data["correctness"]

        # Standardized colors for strategies to maintain visual consistency
        self.colors = {
            "Brute_Force": "#E64242",
            "Only_Sorting": "#EB9035",
            "Only_Heuristic": "#3F98F1",
            "A_Star_Optimized": "#38ED38",
        }

        # Create the directory for saving the plots
        self.output_dir = "tests/results/plots"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all_plots(self):
        """Generates, saves, and displays all significant plots in sequence."""
        self.print_correctness_report()
        self.plot_time_boxplot()
        self.plot_completion_rate()
        self.plot_time_by_grid_size()
        self.plot_time_by_topology()
        self.plot_branches_cut_efficiency()
        self.plot_anytime_behavior()

    def print_correctness_report(self):
        """
        Prints a console report on the validity of symmetry.
        Checks if the path cost from A->B is equal to B->A.
        """
        if not self.correctness_data:
            print("\n[!] No correct data available.")
            return

        total = len(self.correctness_data)
        passed = sum(1 for d in self.correctness_data if d["is_correct"])

        print("\n" + "=" * 50)
        print("CORRECTNESS REPORT (Symmetry O->D == D->O)")
        print("=" * 50)
        print(f"Tests passed: {passed} out of {total} ({(passed / total) * 100:.1f}%)")

        failed = [d for d in self.correctness_data if not d["is_correct"]]
        if failed:
            print("\n[!] Failure details:")
            for f in failed:
                print(
                    f"  - Grid {f['grid_size']}, Topology {f['topology']}, Seed {f['seed']}: Dir={f['cost_dir']} | Rev={f['cost_rev']}"
                )
        else:
            print("All symmetrical paths are correct!")
        print("=" * 50 + "\n")

    def _get_strategies(self) -> list:
        """
        Helper method to extract all unique strategies from the performance data.

        Returns:
            list: A list of strategy names (strings).
        """
        return list(set(d["strategy"] for d in self.performance_data))

    def plot_time_boxplot(self):
        """
        1. Time Distribution (Boxplot)
        Highlights execution time variance, medians, and outliers across strategies.
        """
        strategies = self._get_strategies()
        data_by_strat = {s: [] for s in strategies}

        for d in self.performance_data:
            data_by_strat[d["strategy"]].append(d["time_seconds"])

        plt.figure(figsize=(10, 6))

        # Create boxplot with patch_artist to allow face color filling
        bplot = plt.boxplot([data_by_strat[s] for s in strategies], patch_artist=True)

        # Set X-axis labels manually (compatible with all Matplotlib versions)
        plt.xticks(range(1, len(strategies) + 1), strategies)

        # Apply specific colors to each box based on the strategy
        for patch, color in zip(
            bplot["boxes"], [self.colors.get(s, "gray") for s in strategies]
        ):
            patch.set_facecolor(color)

        plt.title(
            "Execution Time Distribution (Variance)",
            fontsize=14,
            fontweight="bold",
        )
        plt.ylabel("Time (seconds) - Logarithmic Scale", fontsize=12)
        plt.yscale("log")
        plt.grid(True, axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Save and show the plot
        plt.savefig(os.path.join(self.output_dir, "time_boxplot.png"), dpi=300)
        plt.show()

    def plot_completion_rate(self):
        """
        2. Completion Rate
        Displays how often each algorithm successfully finishes before hitting the timeout limit.
        """
        strategies = self._get_strategies()
        rates = {}

        for strat in strategies:
            strat_data = [d for d in self.performance_data if d["strategy"] == strat]
            if not strat_data:
                continue
            completed = sum(1 for d in strat_data if not d["interrupted"])
            rates[strat] = (completed / len(strat_data)) * 100

        plt.figure(figsize=(10, 6))
        strat_names = list(rates.keys())
        rate_values = list(rates.values())

        bars = plt.bar(
            strat_names,
            rate_values,
            color=[self.colors.get(s, "gray") for s in strat_names],
        )

        plt.title(
            "Reliability: % Completion within Timeout",
            fontsize=14,
            fontweight="bold",
        )
        plt.ylabel("Success Rate (%)", fontsize=12)
        plt.ylim(0, 110)

        # Add percentage labels on top of the bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, yval + 2, f"{yval:.1f}%", ha="center"
            )

        plt.tight_layout()

        # Save and show the plot
        plt.savefig(os.path.join(self.output_dir, "completion_rate.png"), dpi=300)
        plt.show()

    def plot_time_by_grid_size(self):
        """
        3. Scalability
        Shows how the execution time grows as the map dimensions increase.
        """
        strategies = self._get_strategies()
        grid_sizes = sorted(
            list(set(d["grid_size"] for d in self.performance_data)),
            key=lambda x: int(x.split("x")[0]),
        )

        plt.figure(figsize=(10, 6))

        for strat in strategies:
            avg_times = []
            for gs in grid_sizes:
                times = [
                    d["time_seconds"]
                    for d in self.performance_data
                    if d["strategy"] == strat and d["grid_size"] == gs
                ]
                avg_times.append(np.mean(times) if times else 0)

            plt.plot(
                grid_sizes,
                avg_times,
                marker="o",
                linewidth=2,
                label=strat,
                color=self.colors.get(strat, "gray"),
            )

        plt.title(
            "Spatial Scalability (Time vs Grid Size)",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Grid Size", fontsize=12)
        plt.ylabel("Average Time (seconds)", fontsize=12)
        plt.yscale("log")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Save and show the plot
        plt.savefig(os.path.join(self.output_dir, "time_by_grid_size.png"), dpi=300)
        plt.show()

    def plot_time_by_topology(self):
        """
        4. Topological Sensitivity
        Analyzes which map obstacles/topologies challenge the algorithms the most.
        """
        strategies = self._get_strategies()
        topologies = list(set(d["topology"] for d in self.performance_data))

        x = np.arange(len(topologies))
        width = 0.2  # Bar width

        plt.figure(figsize=(12, 6))

        for i, strat in enumerate(strategies):
            avg_times = []
            for topo in topologies:
                times = [
                    d["time_seconds"]
                    for d in self.performance_data
                    if d["strategy"] == strat and d["topology"] == topo
                ]
                avg_times.append(np.mean(times) if times else 0)

            offset = (i - len(strategies) / 2) * width + width / 2
            plt.bar(
                x + offset,
                avg_times,
                width,
                label=strat,
                color=self.colors.get(strat, "gray"),
            )

        plt.title("Complexity by Obstacle Topology", fontsize=14, fontweight="bold")
        plt.xlabel("Topology", fontsize=12)
        plt.ylabel("Average Time (seconds)", fontsize=12)
        plt.xticks(x, topologies, rotation=45)
        plt.yscale("log")
        plt.legend()
        plt.tight_layout()

        # Save and show the plot
        plt.savefig(os.path.join(self.output_dir, "time_by_topology.png"), dpi=300)
        plt.show()

    def plot_branches_cut_efficiency(self):
        """
        5. Heuristic Efficiency
        Visualizes the average number of useless branches pruned by each strategy.
        """
        strategies = self._get_strategies()
        avg_cuts = {}

        for strat in strategies:
            cuts = [
                d["branches_cut"]
                for d in self.performance_data
                if d["strategy"] == strat
            ]
            avg_cuts[strat] = np.mean(cuts) if cuts else 0

        plt.figure(figsize=(10, 6))
        strat_names = list(avg_cuts.keys())
        cut_values = list(avg_cuts.values())

        bars = plt.bar(
            strat_names,
            cut_values,
            color=[self.colors.get(s, "gray") for s in strat_names],
        )

        plt.title("Pruning Efficiency (Branch & Bound)", fontsize=14, fontweight="bold")
        plt.ylabel("Average Number of Pruned Branches", fontsize=12)
        plt.yscale("log")  # A* cuts will be astronomically higher than Brute Force

        # Add values on top of the bars
        for bar in bars:
            yval = bar.get_height()
            if yval > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval,
                    f"{int(yval)}",
                    ha="center",
                    va="bottom",
                )

        plt.tight_layout()

        # Save and show the plot
        plt.savefig(
            os.path.join(self.output_dir, "branches_cut_efficiency.png"), dpi=300
        )
        plt.show()

    def plot_anytime_behavior(self):
        """
        6. Anytime Behavior
        Plots the cost of the path found based on the allowed execution time (timeout limit).
        """
        # Filter only executions where a valid path was found
        valid_data = [d for d in self.performance_data if d["cost"] != -1]
        if not valid_data:
            return

        strategies = self._get_strategies()
        timeouts = sorted(list(set(d["timeout_limit"] for d in valid_data)))

        plt.figure(figsize=(10, 6))

        for strat in strategies:
            avg_costs = []
            valid_timeouts = []
            for t in timeouts:
                costs = [
                    d["cost"]
                    for d in valid_data
                    if d["strategy"] == strat and d["timeout_limit"] == t
                ]
                if costs:
                    avg_costs.append(np.mean(costs))
                    valid_timeouts.append(t)

            if valid_timeouts:
                # Use step(where='post') to show that the cost "steps down" over time
                plt.step(
                    valid_timeouts,
                    avg_costs,
                    where="post",
                    marker="o",
                    linewidth=2,
                    label=strat,
                    color=self.colors.get(strat, "gray"),
                )

        plt.title(
            "Anytime Profile (Solution Cost vs Allowed Time)",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Allowed Timeout (seconds)", fontsize=12)
        plt.ylabel("Found Path Cost (lower is better)", fontsize=12)
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Save and show the plot
        plt.savefig(os.path.join(self.output_dir, "anytime_behavior.png"), dpi=300)
        plt.show()
