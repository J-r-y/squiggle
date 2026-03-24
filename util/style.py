from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Sequence

import pygame as pg


@dataclass
class Style:
    width: Optional[int | float] = None
    height: Optional[int | float] = None
    direction: Literal["col", "row"] = "row"
    bg: (
        str
        | pg.Color
        | tuple[int, int, int]
        | tuple[int, int, int, int]
        | Sequence[int]
    ) = field(default_factory=lambda: pg.color.Color("white"))
    border_radius: int = 12

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)
