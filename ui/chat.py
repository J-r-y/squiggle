import pygame as pg

from ui.drawable import Drawable
from util.style import Style


class Chat(Drawable):
    def __init__(self, font: pg.font.Font, style: Style = Style()):
        super().__init__(style)

        self.padding = 5

        self.messages = []

        self.font = pg.font.Font("Poppins.ttf", 16)

    def update(self, e: pg.event.Event): ...

    def add_message(self, name: str, msg: str):
        self.messages.append((name, msg))

    def draw(self, surf: pg.Surface):
        super().draw(surf)
        y = self.rect.bottom
        for i, msg in enumerate(self.messages[::-1]):
            msg_surf = self.render_message(*msg)
            y -= msg_surf.get_height() + self.padding
            surf.blit(msg_surf, (self.rect.x + self.padding, y))

    def render_message(self, name: str, msg: str) -> pg.Surface:
        text = f"{name}: {msg}"
        available = self.rect.w - self.padding * 2
        w, h = self.font.size(text)
        space, _ = self.font.size(" ")
        x, y = self.padding, self.padding

        surf = pg.Surface(
            (
                self.rect.w - self.padding * 2,
                (w // available + 1) * h + self.padding * 2,
            ),
            pg.SRCALPHA,
        )
        pg.draw.rect(
            surf,
            pg.Color("pink"),
            surf.get_rect(),
            border_radius=8,
        )

        for w in text.split(" "):
            render = self.font.render(w, True, "black")
            width = render.get_width() + space
            if x + width > available:
                y += h
                x = space
            surf.blit(render, (x, y))
            x += width

        return surf
