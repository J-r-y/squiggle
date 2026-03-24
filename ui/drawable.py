from typing import TypeVar

import pygame as pg

from util.style import Style


class Drawable:
    def __init__(
        self,
        style: Style = Style(),
        rect: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        self.style = style
        self.rect = pg.Rect(*rect)
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.update_image()

    def update_position(self, *pos):
        self.rect.topleft = pos

    def update_image(self):
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(
            self.image,
            self.style["bg"],
            (0, 0, *self.rect.size),
            border_radius=self.style["border_radius"],
        )
        self.draw_border()

    def draw_border(self):
        pg.draw.rect(
            self.image,
            pg.Color("black"),
            (0, 0, *self.rect.size),
            2,
            border_radius=self.style["border_radius"],
        )

    def update(self, e: pg.event.Event): ...

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)


T = TypeVar("T", bound=Drawable)
