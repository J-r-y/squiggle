import pygame as pg


class Drawable:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        bg: pg.Color | str = pg.Color("white"),
        border_radius: int = 12,
    ):
        self.rect = pg.Rect(x, y, w, h)
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        pg.draw.rect(
            self.image,
            bg,
            (0, 0, w, h),
            border_radius=border_radius,
        )
        pg.draw.rect(
            self.image,
            pg.Color("black"),
            (0, 0, w, h),
            2,
            border_radius=border_radius,
        )

    def update(self, e: pg.event.Event): ...

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)
