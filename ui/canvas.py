from typing import Callable
import json

import pygame as pg

from ui.drawable import Drawable
from ui.palette import Palette
from util.style import Style


class Canvas(Drawable):
    def __init__(
        self, palette: Palette, send_callback: Callable, style: Style = Style()
    ):
        super().__init__(style) if style else super().__init__()

        self.palette = palette
        self.callback = send_callback

        self.active = False
        self.can_draw = True

    def draw_pen(self, pos: tuple[int, int]):
        color = self.palette.color_picker.color
        width = self.palette.slider.width
        self.draw_circle(pos, color, width)

        data = json.dumps(
            {
                "type": "canvas",
                "event": (pos, color, width),
            }
        ).encode()
        self.callback(data)

    def draw_circle(
        self, pos: tuple[int, int], color: str | tuple[int, int, int], width: int, c=5
    ):
        pg.draw.circle(
            self.image,
            pg.Color(color),
            (
                min(max(pos[0] - self.rect.x, c), self.rect.width - c),
                min(max(pos[1] - self.rect.y, c), self.rect.height - c),
            ),
            width,
        )

    def update(self, e: pg.event.Event):
        self.palette.update(e)
        if self.can_draw:
            if e.type == pg.MOUSEMOTION:
                if self.active:
                    self.draw_pen(e.pos)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(e.pos):
                    self.active = True
                    self.draw_pen(e.pos)
            elif e.type == pg.MOUSEBUTTONUP:
                self.active = False

    def draw(self, surf: pg.Surface):
        super().draw(surf)
        self.palette.draw(surf)
