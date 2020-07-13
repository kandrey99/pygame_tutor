import random
import itertools


class GameMap:
    def __init__(self, size):
        self._size = size
        self._grid = self._create_map()

    def _create_map(self):
        coordinates = itertools.product(range(self._size), repeat=2)
        return {coord: random.random() < 0.3 for coord in coordinates}
