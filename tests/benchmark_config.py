from dataclasses import dataclass, field


@dataclass
class TopologyConfig:
    name: str
    base_counts: dict[str, int]
    ref_size: tuple[int, int] = (10, 10)

    def get_counts(self, width: int, height: int) -> dict[str, int]:
        """
        Scala i conteggi degli ostacoli proporzionalmente all'area della mappa.
        Restituisce sempre valori interi (int) maggiori o uguali a 1.
        """
        ref_w, ref_h = self.ref_size
        ref_area = ref_w * ref_h
        current_area = width * height
        ratio = current_area / ref_area

        scaled_counts: dict[str, int] = {}
        for obstacle_type, base_qty in self.base_counts.items():
            if base_qty <= 0:
                continue
            qty = max(1, round(base_qty * ratio))
            scaled_counts[obstacle_type] = int(qty)

        return scaled_counts


@dataclass
class BenchmarkSuiteConfig:
    """Configurazione globale della suite di test."""

    seeds: list[int] = field(default_factory=lambda: list(range(42, 57)))

    # Progressioni dimensionali ben distanziate
    grid_sizes: list[tuple[int, int]] = field(
        default_factory=lambda: [
            (10, 10),
            (12, 12),
            (14, 14),
            (16, 16),
            (18, 18),
            (20, 20),
        ]
    )

    # Watchdog timeout unico per singolo test (in secondi)
    timeout_seconds: int = 15

    topologies: list[TopologyConfig] = field(
        default_factory=lambda: [
            TopologyConfig("Only_Bars", {"Bar": 5}),
            TopologyConfig("Only_Enclosure", {"Enclosure": 5}),
            TopologyConfig("Only_Random", {"Random": 5}),
            TopologyConfig("Only_Diagonal", {"Diagonal": 5}),
            TopologyConfig("Only_Agglomerate", {"Agglomerate": 5}),
            TopologyConfig(
                "Mixed",
                {
                    "Bar": 3,
                    "Enclosure": 2,
                    "Random": 4,
                    "Diagonal": 2,
                    "Agglomerate": 2,
                },
            ),
        ]
    )

    strategies: dict[str, dict[str, bool]] = field(
        default_factory=lambda: {
            "Brute_Force": {"use_heuristic": False, "use_sorting": False},
            "Only_Sorting": {"use_heuristic": False, "use_sorting": True},
            "Only_Heuristic": {"use_heuristic": True, "use_sorting": False},
            "A_Star_Optimized": {"use_heuristic": True, "use_sorting": True},
        }
    )
