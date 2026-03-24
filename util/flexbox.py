import pygame as pg

from ui.drawable import T
from util.style import Style


class Flexbox:
    def __init__(
        self,
        items: tuple[T | Flexbox, ...],
        rect: tuple[int, int, int, int] = (0, 0, 0, 0),
        style: Style = Style(direction="row"),
    ):
        self.rect = pg.rect.Rect(rect)
        self.style = style
        self.gap = 10
        self.grid: list[T | Flexbox] = list(items)
        self.filled_space = (0, 0)

    def add_items(self, *items: T | Flexbox):
        for item in items:
            self.grid.append(item)
        self.set_positions()

    def setup(self):
        self.center((1280, 720))
        self.set_sizes()
        self.set_positions()

    def center(self, space: tuple[int, int]):
        self.rect.center = (space[0] // 2, space[1] // 2)

    def get_space(self) -> tuple[int, int]:
        return (
            self.rect.width - (len(self.grid) - 1) * self.gap,
            self.rect.height - (len(self.grid) - 1) * self.gap,
        )

    def set_positions(self, pos: tuple[int, int] = (0, 0)):
        if pos[0] or pos[1]:
            x, y = pos
        else:
            x, y = self.rect.topleft
        for item in self.grid:
            if isinstance(item, Flexbox):
                item.set_positions((x, y))
                if self.style["direction"] == "row":
                    x += item.rect.width + self.gap
                else:
                    y += item.rect.height + self.gap
            else:
                item.update_position(x, y)
                if self.style["direction"] == "row":
                    x += item.rect.width + self.gap
                else:
                    y += item.rect.height + self.gap

    def set_sizes(self):
        widths = []
        heights = []
        for item in self.grid:
            w = 0
            h = 0
            if isinstance(item, Flexbox):
                if item.style["width"]:
                    w = int(self.rect.width * item.style["width"])
                    item.rect.width = w
                if item.style["height"]:
                    h = int(self.rect.height * item.style["height"])
                    item.rect.height = h
            elif hasattr(item, "style") and not isinstance(item, Flexbox):
                if item.style["width"]:
                    w = item.style["width"]
                    if 0 < w < 1:
                        w *= self.rect.width
                    item.rect.width = w
                    self.rect.width = max(item.rect.width, self.rect.width)
                if item.style["height"]:
                    h = item.style["height"]
                    if 0 < h < 1:
                        h *= self.rect.height
                    item.rect.height = h
                    self.rect.height = max(item.rect.height, self.rect.height)

            widths.append(w)
            heights.append(h)

        if self.style["direction"] == "row":
            part_width = (
                int(
                    (self.rect.width - sum(widths) - (len(self.grid) - 1) * self.gap)
                    / widths.count(0)
                )
                if 0 in widths
                else 1
            )
            part_height = self.rect.height

            self.filled_space = (
                sum([w if w else part_width for w in widths]),
                part_height,
            )
        else:  # col
            part_width = self.rect.width
            part_height = (
                int(
                    (self.rect.height - sum(heights) - (len(self.grid) - 1) * self.gap)
                    / heights.count(0)
                )
                if 0 in heights
                else 1
            )
            self.filled_space = (
                part_width,
                sum([h if h else part_height for h in heights]),
            )

        for item in self.grid:
            if item.rect.width == 0:
                item.rect.width = part_width
            if item.rect.height == 0:
                item.rect.height = part_height
            if isinstance(item, Flexbox):
                item.set_sizes()
            else:
                item.update_image()

    def iterate(self, func_name: str, args: tuple = ()):
        for item in self.grid:
            if isinstance(item, Flexbox):
                item.iterate(func_name, args)
            else:
                getattr(item, func_name)(*args)

    def update(self, e: pg.event.Event):
        self.iterate("update", (e,))

    def draw(self, surf: pg.Surface):
        self.iterate("draw", (surf,))
