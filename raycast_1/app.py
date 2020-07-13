import pygame as pg
from constants import *
from player import Player
from game_map import GameMap
import math


class App:
    def __init__(self):
        self._size = self._width, self._height = 1200, 800
        self._screen = pg.display.set_mode(self._size)
        self._rect = self._screen.get_rect()
        self._clock = pg.time.Clock()
        self._keys = pg.key.get_pressed()
        self._player = Player(self._rect.center)
        self._map = GameMap((12, 8))

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
        for x, y in self._map._grid:
            pg.draw.rect(self._screen, (64,32,32), (x, y, 100, 100), 1)
        fov = math.pi / 3
        ray_count = 24
        scale = self._width / ray_count
        dfov = fov / ray_count
        x0, y0 = self._player.position[0], self._player.position[1]
        angle = self._player.direction - fov / 2
        dist = ray_count / (2 * math.tan(fov / 2))
        proj_k = dist * 1500
        for ray in range(ray_count + 1):
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            for depth in range(1, 1200, 1):
                x, y = x0 + depth * cos_a, y0 + depth * sin_a
                if (x // 100 * 100, y // 100 * 100) in self._map._grid:
                    h = proj_k / depth
                    pg.draw.rect(self._screen, WHITE, (ray * scale, self._height / 2 - h // 2, scale * 1, h * 1), 1)
                    pg.draw.line(self._screen, (32, 32, 32), self._player.position, (x0 + depth * cos_a, y0 + depth * sin_a))
                    break
            angle += dfov
        self._screen.blit(self._player.image, self._player.rect)
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
