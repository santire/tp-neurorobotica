from dataclasses import dataclass
from .position import Position
import numpy as np


@dataclass(frozen=True)
class TelemetryInfo:
    timer: int
    number: int
    health: int
    power: int
    bearing: float
    body_pos: Position
    # Body Rotation 4x3 matrix
    body_rot: np.matrix

    def __eq__(self, other):
        if not isinstance(other, TelemetryInfo):
            return False
        return (
            self.number,
            self.health,
            self.power,
            round(self.bearing, 2),
            self.body_pos,
            # self.body_rot,
        ) == (
            other.number,
            other.health,
            other.power,
            round(other.bearing, 2),
            other.body_pos,
            # other.body_rot,
        )

    def __str__(self):
        # Calculate the maximum width needed for the box
        max_width = 32
        # max_width = (
        #     max(
        #         len(str(self.timer)),
        #         len(str(self.number)),
        #         len(str(self.health)),
        #         len(str(self.power)),
        #         len(str(round(self.bearing, 2))),
        #         len(str(self.body_pos)),
        #     )
        #     + 19
        # )

        # Create the top border of the box
        top_border = "+" + "-" * (max_width - 2) + "+"

        content = (
            f"| Timer: {self.timer:>{max_width - 11}} |\n"
            f"| Number: {self.number:>{max_width - 12}} |\n"
            f"| Health: {self.health:>{max_width - 12}} |\n"
            f"| Power: {self.power:>{max_width - 11}} |\n"
            f"| Bearing: {round(self.bearing, 2):>{max_width - 13}} |\n"
            f"|                  x: {str(round(self.body_pos.x, 3)):>{max_width - 24}} |\n"
            f"| Body Position -> y: {str(round(self.body_pos.y, 3)):>{max_width - 24}} |\n"
            f"|                  z: {str(round(self.body_pos.z, 3)):>{max_width - 24}} |"
        )

        # Create the bottom border of the box
        bottom_border = "+" + "-" * (max_width - 2) + "+"

        # Combine all parts to form the complete box
        box = f"{top_border}\n{content}\n{bottom_border}"

        return box
