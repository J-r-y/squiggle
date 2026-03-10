from ui.drawable import Drawable


class Canvas(Drawable):
    def __init__(self, x: int, y: int, w: int = 700, h: int = 500):
        super().__init__(x, y, w, h)
