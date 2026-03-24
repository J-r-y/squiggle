import pygame as pg

from ui.drawable import Drawable
from util.style import Style


class Palette(Drawable):
    def __init__(self, style: Style = Style()):
        super().__init__(style)

        self.slider = Slider((self.rect.x + 20, self.rect.y, 200, 40))
        self.color_picker = ColorPicker((self.rect.centerx, self.rect.y, 250, 40))

    def update_position(self, *pos):
        super().update_position(*pos)
        self.slider.update_position(
            self.rect.x + self.rect.width / 4 - self.slider.rect.width / 2,
            self.rect.y + self.rect.height / 2 - self.slider.rect.height / 2,
        )
        self.color_picker.update_position(
            self.rect.centerx + self.rect.width / 4 - self.color_picker.rect.width / 2,
            self.rect.y + self.rect.height / 2 - self.color_picker.rect.height / 2,
        )

    def update(self, e: pg.event.Event):
        self.slider.update(e)

    def draw(self, surf: pg.Surface):
        super().draw(surf)
        self.slider.draw(surf)
        self.color_picker.draw(surf)


class Slider(Drawable):
    def __init__(self, rect: tuple[int, int, int, int]):
        super().__init__(rect=rect)

        self.active = False
        self.range = (4, 20)
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.width = 4
        self.draw_handle()

    def draw_handle(self):
        self.image.fill((0, 0, 0, 0))
        pg.draw.line(
            self.image,
            "black",
            (0, self.rect.height / 2 - 1),
            (self.rect.width, self.rect.height / 2 - 1),
            2,
        )
        pg.draw.circle(
            self.image,
            "black",
            (
                max(
                    self.range[0],
                    min(self.width_to_pos(), self.rect.width - self.range[1]),
                ),
                self.rect.height / 2,
            ),
            self.width,
        )

    def width_to_pos(self) -> int:
        return (
            int(
                (self.width - self.range[0])
                / (self.range[1] - self.range[0])
                * self.rect.width
            )
            + self.width // 2
        )

    def pos_to_width(self, pos: int) -> int:
        return min(
            max(
                self.range[0],
                int(
                    (pos - self.rect.x)
                    / self.rect.width
                    * (self.range[1] - self.range[0])
                )
                + self.range[0],
            ),
            self.range[1],
        )

    def update(self, e: pg.event.Event):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(e.pos):
                self.active = True
                self.width = self.pos_to_width(e.pos[0])
                self.draw_handle()
        elif e.type == pg.MOUSEBUTTONUP:
            self.active = False
        elif e.type == pg.MOUSEMOTION:
            if self.active:
                self.width = self.pos_to_width(e.pos[0])
                self.draw_handle()


class ColorPicker(Drawable):
    def __init__(self, rect: tuple[int, int, int, int]):
        super().__init__(rect=rect)

        self.colors = [
            ("black", "white"),
            ("blue4", "blue"),
            ("green4", "green"),
            ("yellow2", "yellow"),
            ("red4", "red"),
            ("darkorchid4", "darkorchid1"),
        ]
        self.color = "black"
