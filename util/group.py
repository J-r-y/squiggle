import pygame as pg


class Group:
    def __init__(self):
        self.sprites = set()

    def add(self, *sprites):
        for sprite in sprites:
            self.sprites.add(sprite)

    def remove(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def update(self, e: pg.event.Event):
        for sprite in self.sprites:
            sprite.update(e)

    def draw(self, surf: pg.Surface):
        for sprite in self.sprites:
            sprite.draw(surf)
