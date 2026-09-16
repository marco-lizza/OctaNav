from dataclasses import dataclass, field


@dataclass
class GeneratorConfig:
    """
    Configuration parameters for the grid map generator.

    Attributes:
        width (int): The width of the grid (number of columns).
        height (int): The height of the grid (number of rows).
        seed (int | None): The seed for the random number generator to ensure reproducibility.
            If None, a purely random seed is used.
        gui (bool | None): Flag to determine whether to launch the Graphical User Interface.
        obstacle_counts (dict[str, int]): A dictionary mapping the obstacle strategy name
            to the exact number of obstacles of that type to generate.
    """

    width: int = 50
    height: int = 50
    seed: int | None = None
    gui: bool | None = None
    obstacle_counts: dict[str, int] = field(default_factory=dict)
