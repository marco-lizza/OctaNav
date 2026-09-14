from dataclasses import dataclass, field


@dataclass
class GeneratorConfig:
    width: int = 50
    height: int = 50
    seed: int | None = None
    gui: bool | None = None
    # Dizionario che associa il nome della strategia al numero di ostacoli da generare
    obstacle_counts: dict[str, int] = field(default_factory=dict)
