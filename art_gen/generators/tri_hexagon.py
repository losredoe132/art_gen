from generators.art_generator import ArtGenerator
from defintions import HW, GridSize
from svg_colors import SVGNumericColor
import numpy as np
from svg_style import SVGStyle
from basics_geoms import Coordinate, Hexagon, Polygon, SVGObject
import math


class TriHexagon(SVGObject):
    def __init__(
        self,
        base: Coordinate,
        R: float,
        styles: tuple[SVGStyle, SVGStyle, SVGStyle],
        inverted: bool = False,
    ):
        super().__init__(SVGStyle())
        self.base = base
        self.inverted = inverted
        self.offset = 1 if self.inverted else 0
        self.R = R
        self.hexagon = Hexagon(self.base, self.R, self.style)
        self.child_elements = [
            self.hexagon,
            Polygon(
                [
                    self.hexagon.base,
                    self.hexagon.points[-0 + self.offset],
                    self.hexagon.points[-1 + self.offset],
                    self.hexagon.points[-2 + self.offset],
                ],
                style=styles[0],
            ),
            Polygon(
                [
                    self.hexagon.base,
                    self.hexagon.points[-2 + self.offset],
                    self.hexagon.points[-3 + self.offset],
                    self.hexagon.points[-4 + self.offset],
                ],
                style=styles[1],
            ),
            Polygon(
                [
                    self.hexagon.base,
                    self.hexagon.points[-4 + self.offset],
                    self.hexagon.points[-5 + self.offset],
                    self.hexagon.points[-0 + self.offset],
                ],
                style=styles[2],
            ),
            # Circle(self.base, r=self.R, style=SVGStyle(stroke_opacity=0.3)),  # r
            # Circle(self.base, r=self.R / math.cos(math.radians(30))),  # R
        ]


class HexagonArtGenerator(ArtGenerator):
    def __init__(self, size: HW, seed: int):
        super().__init__(size)
        np.random.seed(seed)
        self.rand_nums = np.random.randn(3, 3, 2, 2)
        self.grid_size = GridSize(16, 16)
        self.svg_objects: list[SVGObject] = self.generate()

    def generate(self) -> list[SVGObject]:
        R: int = 1000
        r: int = R * math.cos(math.radians(30))
        distance = Coordinate(0.5 * R, 0.5 * r)

        offset = Coordinate(1400, 1400)
        svg_objects = []
        for column_idx in range(self.grid_size.columns):
            for row_idx in range(self.grid_size.rows):
                if self.is_valid(row_idx, column_idx) and self.is_randomly_selected():
                    base = Coordinate(
                        offset.x + (column_idx * distance.x),
                        offset.y + (row_idx * distance.y),
                    )
                    svg_objects.append(
                        TriHexagon(
                            base=base,
                            R=R,
                            styles=self.get_styles(row_idx, column_idx),
                            inverted=self.is_randomly_inverted(),
                        )
                    )
        return svg_objects

    def is_randomly_selected(self) -> bool:
        return np.random.rand() > 0.1

    def is_randomly_inverted(self) -> bool:
        return np.random.rand() > 0.3

    def is_valid(self, row_idx, column_idx) -> bool:
        if (row_idx % 4 == 0) and (column_idx % 6 == 0):
            return True
        elif row_idx % 4 == 2 and column_idx % 6 == 3:
            return True
        else:
            return False

    def get_styles(self, row_idx, column_idx) -> list[SVGNumericColor]:
        styles = []
        for side_idx in range(3):  # for each side of the TripleHexagon
            rgb_vals = []
            for color_channel_idx in range(3):
                channel_val = np.polyval(
                    self.rand_nums[side_idx][color_channel_idx][0],
                    row_idx / self.grid_size.rows,
                )
                row_val = np.polyval(
                    self.rand_nums[side_idx][color_channel_idx][1],
                    column_idx / self.grid_size.columns,
                )
                val = int(127 + ((channel_val + row_val) / 2) * 255)
                rgb_vals.append(val)
            styles.append(SVGStyle(fill=SVGNumericColor(*rgb_vals)))
        return styles
