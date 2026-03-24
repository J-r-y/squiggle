from typing import Callable
import pygame as pg

from ui.drawable import Drawable
from util.style import Style


class Textfield(Drawable):
    def __init__(
        self,
        callback: Callable,
        font: pg.font.Font,
        placeholder: str,
        style: Style = Style(),
    ):
        super().__init__(style)

        self.callback = callback
        self.font = font
        self.placeholder = placeholder
        self.active = False
        self.text = ""

    def update(self, e: pg.event.Event):
        if e.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(e.pos):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_IBEAM)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        elif e.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(e.pos)

        elif e.type == pg.KEYDOWN:
            if self.active:
                if e.key == pg.K_BACKSPACE:
                    if e.mod & pg.KMOD_CTRL:
                        self.text = self.text.rstrip()
                        i = self.text.rfind(" ")
                        if i == -1:
                            self.text = ""
                        else:
                            self.text = self.text[: i + 1]
                    else:
                        self.text = self.text[:-1]
                elif e.key == pg.K_RETURN:
                    self.callback(self.text)
                    self.text = ""
                elif e.unicode.isprintable():
                    self.text += e.unicode

    def draw(self, surf: pg.Surface, dt: int = 1000 // 60):
        super().draw(surf)
        render = self.font.render(
            self.text if len(self.text) else self.placeholder, True, "black"
        )
        x = self.rect.x + 5
        if render.get_width() > self.rect.width - 10:
            for i in range(12, len(self.text)):
                text = self.text[-i - 1 :]
                if self.font.size(text)[0] > self.rect.width - 6:
                    render = self.font.render(self.text[-i:], True, "black")
                    x -= render.get_width() - self.rect.width + 10
                    break

        surf.blit(
            render,
            (
                x,
                self.rect.y + self.rect.height / 2 - render.get_height() / 2,
            ),
        )

        if self.active:
            if (pg.time.get_ticks() // 500) % 2:
                pg.draw.rect(
                    surf,
                    "black",
                    pg.Rect(
                        x + render.get_width() if len(self.text) else x,
                        self.rect.y + 8,
                        4,
                        self.rect.height - 16,
                    ),
                    border_radius=4,
                )
