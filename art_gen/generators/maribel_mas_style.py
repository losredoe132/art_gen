from generators.art_generator import ArtGenerator
from svg_style import SVGStyle
from basics_geoms import Coordinate, SVGObject

from defintions import HW, GridSize
import numpy as np
from dataclasses import dataclass


class MaribelMasGenerator(ArtGenerator):
    def __init__(self, size: HW, seed: int) -> None:
        super().__init__(size)
        np.random.seed(seed)
        self.rand_nums = np.random.randn(3, 3, 2, 2)
        self.grid_size = GridSize(16, 16)
        self.svg_objects = self.generate()

    def generate(self) -> list[SVGObject]:
        return [
            SVGPath(
                start=Coordinate(1000, 1000),
                points=[
                    BezierPoints(
                        Coordinate(1200, 1600),
                        Coordinate(2000, 2000),
                        Coordinate(2000, 1000),
                    ),
                    BezierPoints(
                        Coordinate(2200, 2600),
                        Coordinate(1000, 2000),
                        Coordinate(2000, 1000),
                    ),
                ],
                closed=False,
                style=SVGStyle(fill=None),
            )
        ]


@dataclass
class BezierPoints:
    point: Coordinate
    control_point_0: Coordinate
    control_point_1: Coordinate


class SVGPath(SVGObject):
    def __init__(
        self,
        start: Coordinate,
        points: list[BezierPoints],
        closed: bool,
        style: None | SVGStyle = None,
    ) -> None:
        super().__init__(
            style,
        )
        self.start = start
        self.points = points
        self.closed = closed

    def render(
        self,
    ):
        rendered_str = f'<path d = "M {self.start.x} {self.start.y}'
        for idx, point in enumerate(self.points):
            char = "C" if idx == 0 else "Spline"
            rendered_str += f"{char} {point.control_point_0.x} {point.control_point_0.y} {point.control_point_1.x} {point.control_point_1.y} {point.point.x} {point.point.y} "
        if self.closed:
            rendered_str += " Z "
        rendered_str += ' " '
        rendered_str += self.style.get_str()
        rendered_str += "/>"
        return rendered_str
