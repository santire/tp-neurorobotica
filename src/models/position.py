from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float
    z: float

    def __str__(self):
        return f"(x: {round(self.x, 3)}, y: {round(self.y, 3)}, z: {round(self.z, 3)})"
