import math
from dataclasses import dataclass

from map_generator.models.coordinate import Coordinate
from map_generator.models.grid import Grid
from navigator.path_calculators.type_1_strategy import Type1Strategy
from navigator.path_calculators.type_2_strategy import Type2Strategy


@dataclass
class FreePathResult:
    """
    Data Transfer Object (DTO) containing the evaluated paths and valid dlib.
    """

    type_1_path: list[Coordinate] | None
    type_2_path: list[Coordinate] | None
    dlib: float | None


class PathEngine:
    """
    Core engine orchestrating path strategies and managing results memoization.
    Calculates dynamic properties like dlib only when paths are available.
    """

    def __init__(self, grid: Grid):
        """
        Initializes the engine with the required strategies and an empty cache.
        """
        self.grid = grid
        self._cache: dict[tuple[Coordinate, Coordinate], FreePathResult] = {}

        # Inject strategies
        self._type_1_algo = Type1Strategy()
        self._type_2_algo = Type2Strategy()

    def get_path_from_landmarks(
        self, landmarks: list[tuple[Coordinate, int]]
    ) -> list[Coordinate]:
        path = [landmarks[0][0]]
        for landmark_index in range(len(landmarks) - 1):
            if landmarks[landmark_index + 1][1] == 1:
                path_type_1 = self._type_1_algo.compute(
                    self.grid,
                    landmarks[landmark_index][0],
                    landmarks[landmark_index + 1][0],
                )
                if path_type_1 != None:
                    path.extend(path_type_1[1:])
            if landmarks[landmark_index + 1][1] == 2:
                path_type_2 = self._type_2_algo.compute(
                    self.grid,
                    landmarks[landmark_index][0],
                    landmarks[landmark_index + 1][0],
                )
                if path_type_2 != None:
                    path.extend(path_type_2[1:])

        return path

    def get_paths_and_distance(
        self, origin: Coordinate, destination: Coordinate
    ) -> FreePathResult:
        """
        Retrieves path computations and free distance, utilizing cache if available.
        """
        cache_key = (origin, destination)

        # 1. Memoization Hit
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 2. Delegate to Strategies
        path_1 = self._type_1_algo.compute(self.grid, origin, destination)
        path_2 = self._type_2_algo.compute(self.grid, origin, destination)

        # 3. Domain Logic: dlib exists ONLY if at least one free path exists
        dlib = None
        if path_1 is not None or path_2 is not None:
            dlib = self._compute_theoretical_dlib(origin, destination)

        # 4. Cache and Return
        result = FreePathResult(type_1_path=path_1, type_2_path=path_2, dlib=dlib)
        self._cache[cache_key] = result
        return result

    def _compute_theoretical_dlib(
        self, origin: Coordinate, destination: Coordinate
    ) -> float:
        """Internal pure math calculation of Free Distance."""
        dx = abs(destination.x - origin.x)
        dy = abs(destination.y - origin.y)
        d_min = min(dx, dy)
        d_max = max(dx, dy)
        return math.sqrt(2) * d_min + d_max - d_min
