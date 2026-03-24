import pygame as pg

from ui.drawable import Drawable
from util.style import Style


class Menu(Drawable):
    def __init__(self, style: Style = Style()):
        super().__init__(style)
