import math
from struct import pack
from typing import Tuple

from TelemetryDictionary import telemetrydirs


class Tank:
    def __init__(self, id: int):
        self.id = id
        self.thrust = 0.0
        self.roll = 0.0
        self.precesion = 0.0
        self.pitch = 0.0
        self.shooting = 0  # command
        self.timer = -1
        self.x = None
        self.z = None
        self.bearing = None
        self.health = 1000
        self.last_health = 1000
        self.power = 1000

    def accelerate(self, thrust: float):
        self.thrust += thrust

    def desacelerate(self, thrust: float):
        self.thrust -= thrust

    def reverse(self, thrust: float):
        self.thrust = -thrust

    def turn_left(self, turn: int):
        self.roll = -turn

    def turn_right(self, turn: int):
        self.roll = turn

    def shoot(self):
        self.shooting = 11

    def is_hit(self) -> bool:
        return self.health != self.last_health

    def is_on_edge(self) -> bool:
        vec2d = (float(self.x), float(self.z))
        distance = math.sqrt(vec2d[0] ** 2 + vec2d[1] ** 2)
        return distance >= 1700

    def to_telemetry(self) -> bytes:
        return pack("iffffffiLiiifffi?i",
                    self.id, self.thrust, self.roll,
                    self.pitch, 0.0, self.precesion,
                    0.0, 1, self.timer,
                    self.shooting, 0, 0,
                    self.x, 0.0, self.z,
                    0, 0, 0)

    def update(self, new_values: Tuple):
        self.last_health = self.health
        self.x = new_values[telemetrydirs['x']]
        self.z = new_values[telemetrydirs['z']]
        self.timer = new_values[telemetrydirs['timer']]
        self.power = telemetrydirs['power']
        self.health = telemetrydirs['health']
        self.bearing = telemetrydirs['bearing']
