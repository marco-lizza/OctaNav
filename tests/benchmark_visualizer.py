import os

import matplotlib.pyplot as plt
import numpy as np


class BenchmarkVisualizer:
    """Generatore di grafici scientifici (IEEE/ACM style) per benchmark algoritmici."""

    def __init__(self, data: dict, output_dir: str = "tests/results/plots"):
        self.performance_data = data.get("performance", [])
        self.correctness_data = data.get("correctness", [])
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Palette Okabe-Ito (Colorblind-Safe, adatta a pubblicazioni)
        self.colors = {
            "Brute_Force": "#D55E00",  # Vermillion
            "Only_Sorting": "#E69F00",  # Ochre/Orange
            "Only_Heuristic": "#56B4E9",  # Sky Blue
            "A_Star_Optimized": "#009E73",  # Bluish Green
        }
        self.markers = {
            "Brute_Force": "s",
            "Only_Sorting": "^",
            "Only_Heuristic": "D",
            "A_Star_Optimized": "o",
        }

        # Configurazione tipografica e stilistica globale
        self._apply_scientific_style()

    def _apply_scientific_style(self):
        """Imposta parametri Matplotlib in stile editoriale/accademico."""
        plt.rcParams.update(
            {
                "font.family": "serif",
                "font.serif": [
                    "DejaVu Serif",
                    "Times New Roman",
                    "Computer Modern Roman",
                ],
                "font.size": 10,
                "axes.labelsize": 10.5,
                "axes.titlesize": 11,
                "axes.titleweight": "bold",
                "xtick.labelsize": 9,
                "ytick.labelsize": 9,
                "legend.fontsize": 8.5,
                "figure.titlesize": 12,
                "figure.dpi": 300,
                "savefig.dpi": 300,
                "savefig.bbox": "tight",
                "lines.linewidth": 1.4,
                "lines.markersize": 5,
            }
        )

    def _clean_spines_and_grid(self, ax):
        """Rimuove distrazioni visive e attiva griglie discrete."""
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_linewidth(0.8)
        ax.spines["bottom"].set_linewidth(0.8)
        ax.spines["left"].set_color("#222222")
        ax.spines["bottom"].set_color("#222222")
        ax.grid(
            True, linestyle="--", linewidth=0.5, color="#D0D0D0", alpha=0.7, zorder=0
        )

    def _get_strategies(self) -> list[str]:
        strats = []
        for d in self.performance_data:
            if d["strategy"] not in strats:
                strats.append(d["strategy"])
        return strats

    def _parse_grid_cells(self, grid_str: str) -> int:
        w, h = map(int, grid_str.lower().split("x"))
        return w * h

    def generate_all_plots(self):
        """Esegue l'intera suite di analisi grafica."""
        self.plot_ecdf_cactus()
        self.plot_complexity_scaling_loglog()
        self.plot_topology_profile()
        self.plot_pruning_pareto()
        self.plot_memory_scaling()
        self.plot_space_time_tradeoff()

    def plot_ecdf_cactus(self):
        """Mostra la proporzione cumulativa di istanze risolte in funzione del tempo."""
        strategies = self._get_strategies()
        fig, ax = plt.subplots(figsize=(6, 4))
        self._clean_spines_and_grid(ax)

        for strat in strategies:
            strat_runs = [d for d in self.performance_data if d["strategy"] == strat]
            if not strat_runs:
                continue

            total_runs = len(strat_runs)
            completed_times = np.sort(
                [d["time_seconds"] for d in strat_runs if d["completed"]]
            )

            if len(completed_times) == 0:
                continue

            # Frazione cumulata sul totale reale (inclusi i timeout)
            y_fractions = (np.arange(1, len(completed_times) + 1) / total_runs) * 100

            # Aggiunge punto zero
            x = np.concatenate(([completed_times[0]], completed_times))
            y = np.concatenate(([0], y_fractions))

            ax.step(
                x,
                y,
                where="post",
                label=f"{strat.replace('_', ' ')}",
                color=self.colors.get(strat, "#444444"),
                linewidth=1.6,
                zorder=3,
            )

        ax.set_xscale("log")
        ax.set_ylim(-2, 103)
        ax.set_xlabel("Execution Time $t$ (seconds) [Log Scale]")
        ax.set_ylabel("Instances Solved (%)")
        ax.set_title("Empirical Cumulative Distribution Function (ECDF)")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0", framealpha=0.9)

        plt.savefig(os.path.join(self.output_dir, "fig1_ecdf_cactus.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig1_ecdf_cactus.png"))
        plt.close()

    def plot_complexity_scaling_loglog(self):
        """Visualizza l'andamento asintotico empirico rispetto al numero di nodi N = W * H."""
        strategies = self._get_strategies()
        raw_sizes = list(set(d["grid_size"] for d in self.performance_data))
        sorted_sizes = sorted(raw_sizes, key=self._parse_grid_cells)
        nodes = np.array([self._parse_grid_cells(gs) for gs in sorted_sizes])

        fig, ax = plt.subplots(figsize=(6.5, 4.2))
        self._clean_spines_and_grid(ax)

        for strat in strategies:
            medians = []
            q25_arr = []
            q75_arr = []
            valid_n = []

            for gs, n in zip(sorted_sizes, nodes):
                times = [
                    d["time_seconds"]
                    for d in self.performance_data
                    if d["strategy"] == strat
                    and d["grid_size"] == gs
                    and d["completed"]
                ]
                # Richiede una soglia minima di completamento per tracciare il punto
                if len(times) >= 2:
                    valid_n.append(n)
                    medians.append(np.median(times))
                    q25_arr.append(np.percentile(times, 25))
                    q75_arr.append(np.percentile(times, 75))

            if len(valid_n) >= 2:
                valid_n = np.array(valid_n)
                medians = np.array(medians)
                color = self.colors.get(strat, "#444444")
                marker = self.markers.get(strat, "o")

                # Linea mediana e punti
                ax.plot(
                    valid_n,
                    medians,
                    label=strat.replace("_", " "),
                    color=color,
                    marker=marker,
                    zorder=4,
                )
                # Area di dispersione Interquartile (IQR 25%-75%)
                ax.fill_between(
                    valid_n,
                    q25_arr,
                    q75_arr,
                    color=color,
                    alpha=0.18,
                    zorder=2,
                )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Graph Size $N = |V|$ (Total Grid Cells)")
        ax.set_ylabel("Median Wall-Clock Time (s)")
        ax.set_title("Empirical Computational Complexity ($T$ vs $N$)")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0")

        plt.savefig(os.path.join(self.output_dir, "fig2_scaling_loglog.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig2_scaling_loglog.png"))
        plt.close()

    def plot_topology_profile(self):
        """
        Sostituisce il consueto bar-plot confusionario con un Cleveland Dot Plot
        molto più pulito e leggibile.
        """
        strategies = self._get_strategies()
        topologies = sorted(list(set(d["topology"] for d in self.performance_data)))

        fig, ax = plt.subplots(figsize=(7, 4.5))
        self._clean_spines_and_grid(ax)

        y_positions = np.arange(len(topologies))

        for strat in strategies:
            medians = []
            for topo in topologies:
                times = [
                    d["time_seconds"]
                    for d in self.performance_data
                    if d["strategy"] == strat
                    and d["topology"] == topo
                    and d["completed"]
                ]
                medians.append(np.median(times) if times else np.nan)

            ax.scatter(
                medians,
                y_positions,
                label=strat.replace("_", " "),
                color=self.colors.get(strat, "#333333"),
                marker=self.markers.get(strat, "o"),
                s=40,
                zorder=4,
            )

        ax.set_xscale("log")
        ax.set_yticks(y_positions)
        ax.set_yticklabels(topologies)
        ax.set_xlabel("Median Wall-Clock Time (s) [Log Scale]")
        ax.set_title("Topological Hardness Comparison")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0")

        plt.savefig(os.path.join(self.output_dir, "fig3_topology_hardness.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig3_topology_hardness.png"))
        plt.close()

    def plot_pruning_pareto(self):
        """Scatter plot dei nodi/rami tagliati vs tempo reale per esaminare l'overhead dell'euristica."""
        fig, ax = plt.subplots(figsize=(6, 4))
        self._clean_spines_and_grid(ax)

        for strat in self._get_strategies():
            runs = [
                d
                for d in self.performance_data
                if d["strategy"] == strat and d["completed"] and d["branches_cut"] > 0
            ]
            if not runs:
                continue

            cuts = [d["branches_cut"] for d in runs]
            times = [d["time_seconds"] for d in runs]

            ax.scatter(
                cuts,
                times,
                label=strat.replace("_", " "),
                color=self.colors.get(strat, "#444444"),
                marker=self.markers.get(strat, "o"),
                alpha=0.55,
                s=25,
                edgecolors="none",
                zorder=3,
            )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Search Space Pruned (Branches Cut) [Log Scale]")
        ax.set_ylabel("Execution Time (s) [Log Scale]")
        ax.set_title("Pruning Power vs Computational Speedup")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0")

        plt.savefig(os.path.join(self.output_dir, "fig4_pruning_tradeoff.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig4_pruning_tradeoff.png"))
        plt.close()

    def plot_memory_scaling(self):
        """
        Dimostra come l'occupazione di memoria (KiB) cresce al crescere dell'area della griglia.
        Grafico log-log con banda interquartile (25°-75° percentile).
        """
        strategies = self._get_strategies()
        raw_sizes = list(set(d["grid_size"] for d in self.performance_data))
        sorted_sizes = sorted(raw_sizes, key=self._parse_grid_cells)
        nodes = np.array([self._parse_grid_cells(gs) for gs in sorted_sizes])

        fig, ax = plt.subplots(figsize=(6.5, 4.2))
        self._clean_spines_and_grid(ax)

        for strat in strategies:
            medians = []
            q25_arr = []
            q75_arr = []
            valid_n = []

            for gs, n in zip(sorted_sizes, nodes):
                mems = [
                    d["peak_memory_kb"]
                    for d in self.performance_data
                    if d["strategy"] == strat
                    and d["grid_size"] == gs
                    and d.get("peak_memory_kb") is not None
                ]
                if mems:
                    valid_n.append(n)
                    medians.append(np.median(mems))
                    q25_arr.append(np.percentile(mems, 25))
                    q75_arr.append(np.percentile(mems, 75))

            if valid_n:
                color = self.colors.get(strat, "#444444")
                marker = self.markers.get(strat, "o")
                ax.plot(
                    valid_n,
                    medians,
                    label=strat.replace("_", " "),
                    color=color,
                    marker=marker,
                    zorder=4,
                )
                ax.fill_between(
                    valid_n, q25_arr, q75_arr, color=color, alpha=0.18, zorder=2
                )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Graph Size $N = |V|$ (Total Grid Cells)")
        ax.set_ylabel("Peak Memory Allocation (KiB) [Log Scale]")
        ax.set_title("Spatial Scalability ($M_{\\mathrm{peak}}$ vs $N$)")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0")

        plt.savefig(os.path.join(self.output_dir, "fig_space_1_scaling.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig_space_1_scaling.png"))
        plt.close()

    def plot_space_time_tradeoff(self):
        """
        Scatter plot bi-dimensionale Tempo vs Memoria.
        Identifica quale strategia domina sia nello spazio sia nel tempo (angolo in basso a sinistra).
        """
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        self._clean_spines_and_grid(ax)

        for strat in self._get_strategies():
            runs = [
                d
                for d in self.performance_data
                if d["strategy"] == strat
                and d["completed"]
                and d.get("peak_memory_kb") is not None
            ]
            if not runs:
                continue

            times = [d["time_seconds"] for d in runs]
            mems = [d["peak_memory_kb"] for d in runs]

            ax.scatter(
                times,
                mems,
                label=strat.replace("_", " "),
                color=self.colors.get(strat, "#444444"),
                marker=self.markers.get(strat, "o"),
                alpha=0.6,
                s=35,
                edgecolors="none",
                zorder=3,
            )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Execution Time (s) [Log Scale]")
        ax.set_ylabel("Peak Memory (KiB) [Log Scale]")
        ax.set_title("Space-Time Trade-off (Time vs Memory)")
        ax.legend(frameon=True, facecolor="white", edgecolor="#C0C0C0")

        plt.savefig(os.path.join(self.output_dir, "fig_space_2_tradeoff.pdf"))
        plt.savefig(os.path.join(self.output_dir, "fig_space_2_tradeoff.png"))
        plt.close()
