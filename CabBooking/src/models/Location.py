from __future__ import annotations  # postpone evaluation of annotations
from math import sqrt


class Location:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def distance(self, destination: Location) -> float:
        return sqrt(pow(self.x - destination.x, 2) + pow(self.y - destination.y, 2))
