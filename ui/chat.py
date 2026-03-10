import pygame as pg

from ui.drawable import Drawable


class Chat(Drawable):
    def __init__(self, font: pg.font.Font, x: int, y: int, w: int = 200, h: int = 700):
        super().__init__(x, y, w, h)
        self.padding = 5

        self.messages = [("Me", "Hello world! What is this game even about")]

        self.font = font

    def update(self, e: pg.event.Event): ...

    def add_message(self, name: str, msg: str): ...

    def draw(self, surf: pg.Surface):
        super().draw(surf)
        for msg in self.messages:
            surf.blit(self.render_message(*msg), (10, 10))

    def render_message(self, name: str, msg: str) -> pg.Surface:
        text = f"{name}: {msg}"
        space = self.rect.w - 10
        w, h = self.font.size(text)
        x, y = 5, 5

        surf = pg.Surface((self.rect.w, (w // space + 1) * h + 10), pg.SRCALPHA)
        pg.draw.rect(
            surf,
            pg.Color("pink"),
            surf.get_rect(),
            border_radius=12,
        )

        for w in text.split(" "):
            render = self.font.render(w, True, "black")
            width = render.get_width() + 5
            if x + width > space:
                y += h
                x = 5
            surf.blit(render, (x, y))
            x += width

        return surf
