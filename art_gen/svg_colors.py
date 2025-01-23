from enum import Enum
import numpy as np


class SVGNumericColor:
    def __init__(self, red: int, green: int, blue: int):
        self.red = self._clip(red)
        self.green = self._clip(green)
        self.blue = self._clip(blue)

    def _clip(self, val):
        return np.clip(val, 0, 255)


class SVGColor(Enum):
    BLACK = "black"
    GREY = "grey"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    WHITE = "white"
