import pygame as pg
from constants import *
import math

CIRCLE = 2 * math.pi


class Player:
    def __init__(self, pos, direction=0):
        self._x, self._y = pos
        self._direction = direction
        self._rotate_speed = math.pi / 2
        self._speed = 100

    @property
    def position(self):
        return self._x, self._y

    @property
    def direction(self):
        return self._direction

    def draw(self, sc):
        cos, sin = math.cos(self._direction), math.sin(self._direction)
        pg.draw.circle(sc, GREEN, (int(self._x), int(self._y)), 16, 1)
        pg.draw.line(sc, GREEN, (self._x, self._y), (self._x + 100 * cos, self._y + 100 * sin))

    def rotate(self, angle):
        self._direction = (self._direction + angle) % CIRCLE

    def walk(self, distance):
        cos, sin = math.cos(self._direction), math.sin(self._direction)
        self._x, self._y = self._x + distance * cos, self._y + distance * sin

    def update(self, keys, dt):
        if keys[pg.K_LEFT]:
            self.rotate(-self._rotate_speed * dt)
        if keys[pg.K_RIGHT]:
            self.rotate(self._rotate_speed * dt)
        if keys[pg.K_UP]:
            self.walk(self._speed * dt)
        if keys[pg.K_DOWN]:
            self.walk(-self._speed * dt)
