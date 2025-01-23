from __future__ import annotations
from typing import NamedTuple
import math


from svg_style import SVGStyle


class Coordinate(NamedTuple):
    x: int
    y: int


class SVGObject:
    def __init__(
        self, style: None | SVGStyle, child_elements: None | list[SVGObject] = None
    ) -> None:
        self.style = style if style else SVGStyle()
        self.child_elements = [] if child_elements is None else child_elements

    def render(
        self,
    ) -> str:
        """Renders the Object into plain svg.

        :return: The rendered object
        """
        return " ".join([child.render() for child in self.child_elements])


class Polygon(SVGObject):
    def __init__(self, points: list[Coordinate], style: None | SVGStyle = None) -> None:
        super().__init__(style)
        self.points = points

    def render(self) -> str:
        points_str = " ".join(f"{int(p.x)},{int(p.y)}" for p in self.points)
        return f'<polygon points="{points_str}" {self.style.get_str()} />'


class Circle(SVGObject):
    def __init__(
        self, center: Coordinate, r: float, style: None | SVGStyle = None
    ) -> None:
        super().__init__(style)
        self.center = center
        self.r = r

    def render(self) -> str:
        return f'<circle cx="{self.center.x}" cy="{self.center.y}" r="{self.r}" {self.style.get_str()}/>'


class Spline(SVGObject):
    def __init__(self, points: list[Coordinate], style: None | SVGStyle = None) -> None:
        super().__init__(style)
        self.points = points

    def render(self) -> str:
        points_str = " ".join(f"M{int(p.x)},{int(p.y)}" for p in self.points)
        return f'<path d="{points_str}" {self.style.get_str()} />'


class Hexagon(Polygon):
    points: list[Coordinate]

    def __init__(self, base: Coordinate, R: float, style: SVGStyle):
        """"""
        self.base = base
        self.R = R
        super().__init__(points=self.get_points(), style=style)

    def get_points(self):
        angle = math.pi / 3  # 60 degrees in radians
        points: list[Coordinate] = []
        for i in range(6):
            dist_x = round(self.R * math.cos(i * angle))  #
            dist_y = round(self.R * math.sin(i * angle))  # / math.cos(math.radians(30))
            points.append(Coordinate(self.base.x + dist_x, self.base.y + dist_y))
        return points
