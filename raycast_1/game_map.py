import random
import itertools
from constants import *


class GameMap:
    def __init__(self, size):
        self._size = size
        self.grid = self._create_map()

    def _create_random_map(self):
        coordinates = itertools.product(range(self._size[0]), range(self._size[1]))
        grid = [(coord[0] * 100, coord[1] * 100) for coord in coordinates if random.random() < 0.2]
        return grid

    def _create_map(self):
        plan = ['WWWWWWWWWWWW',
                'W..........W',
                'W.....W....W',
                'W..........W',
                'W..........W',
                'W.WW.......W',
                'W..........W',
                'WWWWWWWWWWWW', ]
        grid = [(column * TILE, row * TILE) for row in range(8) for column in range(12) if plan[row][column] == 'W']
        print(grid)
        return grid
