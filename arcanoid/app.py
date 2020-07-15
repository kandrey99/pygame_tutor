import pygame as pg
# from constants import *
# from player import Player
# from game_map import GameMap
import math

BLACK = (16, 16, 16)


class App:
    def __init__(self):
        self._size = self._width, self._height = 1200, 800
        self._screen = pg.display.set_mode(self._size)
        self._rect = self._screen.get_rect()
        self._clock = pg.time.Clock()
        self._keys = pg.key.get_pressed()

    def _event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type in (pg.KEYUP, pg.KEYDOWN):
                self._keys = pg.key.get_pressed()

    def _update(self, dt):
        pass

    def _render(self):
        self._screen.fill(BLACK)
        pg.display.flip()

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
