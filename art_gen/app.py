from flask import Flask
from defintions import HW
from generators.tri_hexagon import HexagonArtGenerator
from generators.maribel_mas_style import MaribelMasGenerator

app = Flask(__name__, static_folder="static")


@app.route("/hexagon/<int:seed>")
def serve_hexagon(seed):
    return HexagonArtGenerator(HW(1000, 1000), seed=seed).render()


@app.route("/maribel-mas/<int:seed>")
def serve_maribel_mas(seed):
    return MaribelMasGenerator(HW(1000, 1000), seed=seed).render()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
