import random


class GridRandomizer:
    """
    A wrapper around Python's built-in random module to provide controlled,
    seed-based random number generation. Ensures reproducibility across
    different runs when the same seed is used.

    Attributes:
        seed (int | None): The seed value used to initialize the random generator.
    """

    def __init__(self, seed: int | None = None):
        """
        Initializes the randomizer with an optional seed.

        Args:
            seed (int | None): The seed for the random number generator.
                If None, system time or OS-specific randomness is used.
        """
        self.seed = seed
        self._rand = random.Random(seed)

    def set_seed(self, seed: int) -> None:
        """
        Set a new seed.

        Args:
            seed (int): The seed for the random number generator.
        """
        self.seed = seed

    def next_int(self, min_val: int, max_val: int) -> int:
        """
        Generates a random integer between min_val (inclusive) and max_val (exclusive).
        The behavior mirrors C#'s Random.Next(min, max).

        Args:
            min_val (int): The inclusive lower bound.
            max_val (int): The exclusive upper bound.

        Returns:
            int: A random integer in the range [min_val, max_val - 1].
        """
        return self._rand.randrange(min_val, max_val)

    def next_bool(self) -> bool:
        """
        Generates a random boolean value.

        Returns:
            bool: True or False with a 50% probability.
        """
        return self._rand.choice([True, False])
