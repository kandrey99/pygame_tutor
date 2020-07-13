import pygame as pg
from pygame.sprite import Sprite
from constants import *
import math

CIRCLE = 2 * math.pi


class Player(Sprite):
    def __init__(self, pos):
        super().__init__()
        self._position = pos
        self.image = pg.Surface((32, 32)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=pos)
        self._direction = 0
        self._dir_info = math.cos(self._direction), math.sin(self._direction)
        self._rotate_speed = math.pi / 2
        self._speed = 64
        self._draw()

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction

    def _draw(self):
        self.image.fill(BLACK)
        rect = self.image.get_rect()
        pg.draw.circle(self.image, GREEN, rect.center, 16, 1)
        pg.draw.line(self.image, GREEN, rect.center, ((self._dir_info[0] + 1) * 16, (self._dir_info[1] + 1) * 16))

    def rotate(self, angle):
        self._direction = (self._direction + angle) % CIRCLE
        self._dir_info = math.cos(self._direction), math.sin(self._direction)

    def walk(self, distance):
        self._position = (self._position[0] + distance * self._dir_info[0],
                          self._position[1] + distance * self._dir_info[1])
        self.rect.center = self._position

    def update(self, keys, dt):
        if keys[pg.K_LEFT]:
            self.rotate(-self._rotate_speed * dt)
        if keys[pg.K_RIGHT]:
            self.rotate(self._rotate_speed * dt)
        if keys[pg.K_UP]:
            self.walk(self._speed * dt)
        if keys[pg.K_DOWN]:
            self.walk(-self._speed * dt)
        self._draw()
