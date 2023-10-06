from dataclasses import dataclass


@dataclass
class CommandOrder:
    timer: int
    controlling_id: int
    thrust: float
    roll: float
    pitch: float
    yaw: float
    precesion: float
    bank: float
    faction: int
