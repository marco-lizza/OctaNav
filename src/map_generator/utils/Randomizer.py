import random


class Randomizer:
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rand = random.Random(seed)

    def next_int(self, min_val: int, max_val: int) -> int:
        # random.randrange genera un numero tra min_val (incluso) e max_val (escluso), come C#
        return self._rand.randrange(min_val, max_val)

    def next_bool(self) -> bool:
        return self._rand.choice([True, False])
