from defintions import HW
from basics_geoms import SVGObject


from jinja2 import Environment, PackageLoader, select_autoescape


from abc import ABC, abstractmethod


class ArtGenerator(ABC):
    def __init__(self, size: HW):
        self.size = size
        self.env = Environment(
            loader=PackageLoader("app"), autoescape=select_autoescape()
        )
        self.svg_objects: list[SVGObject] = []

    @abstractmethod
    def generate(self) -> list[SVGObject]:
        """Create the SVGObjects to be shown"""

    def render(self) -> str:
        content = " ".join([svg_obj.render() for svg_obj in self.svg_objects])
        return self.env.get_template("base.html.jinja").render(
            height=self.size.height, width=self.size.width, content=content
        )
