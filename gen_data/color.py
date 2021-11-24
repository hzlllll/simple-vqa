from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    TEAL = (0, 128, 128)
    BROWN = (165, 42, 42)


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
