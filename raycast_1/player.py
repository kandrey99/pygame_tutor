import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2
from constants import *
from collections import namedtuple
import math

CIRCLE = 2 * math.pi

DirInfo = namedtuple('DirInfo', 'cos sin')


class Player(Sprite):
    def __init__(self, pos):
        super().__init__()
        self._position = Vector2(pos)
        self.image = pg.Surface((60, 60))
        self.rect = self.image.get_rect(center=pos)
        self._direction = 0
        self._dir_info = DirInfo._make((math.cos(self._direction), math.sin(self._direction)))
        self._rotate_speed = math.pi / 2
        self._speed = 100
        self._draw()

    def _draw(self):
        self.image.fill(BLACK)
        rect = self.image.get_rect()
        pg.draw.circle(self.image, GREEN, rect.center, 30, 1)
        pg.draw.line(self.image, GREEN, rect.center, (30 * (1 + self._dir_info.cos), 30 * (1 + self._dir_info.sin)))

    def rotate(self, angle):
        self._direction = (self._direction + angle) % CIRCLE
        self._dir_info = DirInfo._make((math.cos(self._direction), math.sin(self._direction)))

    def walk(self, distance):
        self._position += self._dir_info.cos * distance, self._dir_info.sin * distance
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
