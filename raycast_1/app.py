import pygame as pg
from constants import *
from player import Player


class App:
    def __init__(self):
        self._size = self._width, self._height = 800, 600
        self._screen = pg.display.set_mode(self._size)
        self._rect = self._screen.get_rect()
        self._clock = pg.time.Clock()
        self._player = Player(self._rect.center)
        self._keys = pg.key.get_pressed()

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
