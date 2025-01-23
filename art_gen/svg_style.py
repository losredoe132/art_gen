from svg_colors import SVGColor, SVGNumericColor


from dataclasses import dataclass, fields
from enum import Enum


@dataclass
class SVGStyle:
    fill: None | SVGColor | SVGNumericColor = None
    stroke: None | SVGColor | SVGNumericColor = SVGColor.BLACK
    stroke_width: int = 10
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0

    def get_str(self):
        style_items = set()
        for f in fields(self):
            k = f.name.replace("_", "-")
            v = getattr(self, f.name)
            if v is not None:
                if isinstance(v, Enum):
                    val = v.value
                elif isinstance(v, SVGNumericColor):
                    val = f"rgb({v.red}, {v.green}, {v.blue})"
                else:
                    val = v
            else:
                val = "None"
            style_items.add(f"{k}:{val};")

        style = " ".join(style_items)
        return f'style ="{style}"'
