from dataclasses import dataclass


@dataclass
class CommandOrder:
    timer: int
    controlling_id: int
    thrust: float
    roll: float
    pitch: float
    x: float
    z: float
    precesion: float
    command: int
    faction: int = 1
    yaw: float = 0.0
    bank: float = 0.0
    spawnid: int = 0
    type_of_island: int = 0
    y: float = 0.0
    bit: int = 0
    target: int = 0
    weapon: int = 0
