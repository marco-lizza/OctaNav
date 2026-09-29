from dataclasses import dataclass, field


@dataclass
class TopologyConfig:
    name: str
    obstacle_counts: dict[str, int]


@dataclass
class BenchmarkSuiteConfig:
    """Global configuration for test suite"""

    seeds: list[int] = field(default_factory=lambda: [42, 43])
    grid_sizes: list[tuple[int, int]] = field(
        default_factory=lambda: [(15, 15), (20, 20)]
    )
    timeout_seconds: list[int] = field(default_factory=lambda: [15, 30])

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
                    "Bar": 2,
                    "Enclosure": 1,
                    "Random": 3,
                    "Diagonal": 3,
                    "Agglomerate": 3,
                },
            ),
            # ... other typology ...
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
