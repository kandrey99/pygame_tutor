import pygame as pg
from pygame.math import Vector2
from constants import *
from player import Player
from game_map import GameMap
import math


class App:
    def __init__(self):
        self._size = self._width, self._height = 800, 600
        self._screen = pg.display.set_mode(self._size)
        self._rect = self._screen.get_rect()
        self._clock = pg.time.Clock()
        self._keys = pg.key.get_pressed()
        self._player = Player(self._rect.center)
        self._map = GameMap(8)

    def _event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type in (pg.KEYUP, pg.KEYDOWN):
                self._keys = pg.key.get_pressed()

    def _update(self, dt):
        self._player.update(self._keys, dt)

    def _render(self):
        self._screen.fill(BLACK)
        self._screen.blit(self._player.image, self._player.rect)
        fov = math.pi / 3
        fov_delta = fov / 120
        angle = self._player.direction - fov / 2
        for i in range(121):
            angle += fov_delta
            v = Vector2(math.cos(angle), math.sin(angle))
            for depth in range(300):
                pg.draw.line(self._screen, GRAY, self._player.position,
                             self._player.position + depth * v)
        for (x, y), v in self._map._grid.items():
            if v:
                pg.draw.rect(self._screen, GRAY, (x * 64, y * 64, 64, 64), 1)

        pg.display.flip()

    def run(self):
        while True:
            dt = self._clock.tick(30) / 1000
            self._event_loop()
            self._update(dt)
            self._render()


if __name__ == '__main__':
    pg.init()
    app = App()
    app.run()
