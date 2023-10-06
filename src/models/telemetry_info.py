from dataclasses import dataclass
from .position import Position
import numpy as np


@dataclass
class TelemetryInfo:
    timer: int
    number: int
    health: int
    power: int
    bearing: float
    body_pos: Position
    # Body Rotation 4x3 matrix
    body_rot: np.matrix
