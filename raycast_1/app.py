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
        self._fov = 2 * math.pi / 6
        self._ray_count = 12
        self._scale = self._width / self._ray_count
        self._dfov = self._fov / (self._ray_count - 1)
        self._dist = self._ray_count / (2 * math.tan(self._fov / 2))
        self._k = 40000 * self._dist / self._ray_count
        self._player = Player(self._rect.center)
        self._game_map = GameMap((12, 8))

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
        # pg.draw.rect(self._screen, (0, 128, 255), (0, 0, self._width, self._height / 2))  # sky
        # pg.draw.rect(self._screen, (16, 64, 16), (0, self._height / 2, self._width, self._height))  # ground
        x0, y0 = self._player.position
        self._ray_cast_3()
        for x, y in self._game_map.grid:
            pg.draw.rect(self._screen, (64, 32, 32), (x, y, TILE, TILE), 1)
        self._player.draw(self._screen)
        pg.display.flip()

    def _ray_cast_1(self):
        x0, y0 = self._player.position
        angle = self._player.direction - self._fov / 2
        for ray in range(self._ray_count):
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            for depth in range(1, 300, 1):
                x, y = x0 + depth * cos_a, y0 + depth * sin_a
                # pg.draw.line(self._screen, (32, 32, 32), self._player.position,
                #              (x0 + depth * cos_a, y0 + depth * sin_a))
                depth *= math.cos(self._player.direction - angle)  # correct fish eye
                # pg.draw.line(self._screen, (32, 32, 32), self._player.position,
                #              (x0 + depth * cos_a, y0 + depth * sin_a))
                if self._map(x, y) in self._game_map.grid:
                    height = self._k / depth
                    c = 255 / (1 + depth ** 2 / 100000)
                    pg.draw.rect(self._screen, (c, c, c),
                                 (ray * self._scale, self._height / 2 - height / 2, self._scale, height), 1)
                    break
            angle += self._dfov

    def _ray_cast_3(self):
        x0, y0 = self._player.position
        xm, ym = self._map(x0, y0)
        angle = self._player.direction - self._fov / 2

        for ray in range(self._ray_count):
            cos_a, sin_a = math.cos(angle) or 0.000001, math.sin(angle) or 0.000001

            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for _ in range(0, self._height, TILE):
                depth_h = (y - y0) / sin_a
                x = x0 + depth_h * cos_a
                if self._map(x, y + dy) in self._game_map.grid or not self._contains(x, y):
                    break
                y += dy * TILE

            x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for _ in range(0, self._width, TILE):
                depth_v = (x - x0) / cos_a
                y = y0 + depth_v * sin_a
                if self._map(x + dx, y) in self._game_map.grid or not self._contains(x, y):
                    break
                x += dx * TILE

            depth = min(depth_v, depth_h)
            pg.draw.line(self._screen, (32, 32, 32), self._player.position, (x0 + depth * cos_a, y0 + depth * sin_a))
            depth *= math.cos(self._player.direction - angle)
            height = self._k / depth
            c = 255 / (1 + depth * depth * 0.000005)
            color = (c, c, c)
            pg.draw.rect(self._screen, color,
                         (ray * self._scale, self._height / 2 - height // 2, self._scale, height), 1)

            angle += self._dfov

    @staticmethod
    def _map(x, y):
        return int(x / TILE) * TILE, int(y / TILE) * TILE

    def _contains(self, x, y):
        return 0 <= x < self._width and 0 <= y < self._height

    def display_fps(self):
        caption = f'FPS: {self._clock.get_fps():.2f}'
        pg.display.set_caption(caption)

    def run(self):
        while True:
            dt = self._clock.tick(300) / 1000
            self._event_loop()
            self._update(dt)
            self._render()
            self.display_fps()


if __name__ == '__main__':
    pg.init()
    app = App()
    app.run()
