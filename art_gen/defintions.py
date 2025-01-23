from typing import NamedTuple

import logging

logger = logging.getLogger(__name__)


class HW(NamedTuple):
    height: int
    width: int


class GridSize(NamedTuple):
    columns: int
    rows: int
