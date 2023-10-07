from typing import List, Tuple
from src.models.position import Position
import numpy as np
import math

rotation_gain = 0.1
thrust_gain = 0.05

max_thrust = 200
max_rotation = 20


def mod(a, n):
    return (a % n + n) % n

def is_in_safe_zone(tank_pos):
    vec2d = (float(tank_pos.x), float(tank_pos.z))
    distance = math.sqrt(vec2d[0] ** 2 + vec2d[1] ** 2)
    return distance <= 1500

def get_tank_params(my_bearing: float, my_pos: Position, enemy_pos: Position) ->  Tuple[float, float, float]:
    relative_pos = Position(x=enemy_pos.x - my_pos.x, y=0, z=enemy_pos.z - my_pos.z)

    desired_bearing = np.rad2deg(
        math.atan2(relative_pos.z, relative_pos.x) - math.pi / 2
    )
    heading_error = desired_bearing - my_bearing
    heading_error = mod((heading_error + 180), 360) - 180
    print(f"heading_error: {heading_error}")

    roll = min(max_rotation, max(-max_rotation, rotation_gain * heading_error))

    distance_to_target = math.sqrt(relative_pos.x**2 + relative_pos.z**2)
    thrust = thrust_gain * distance_to_target
    print(f"distance to target: {distance_to_target}")
    return thrust, roll, distance_to_target


def get_turret_params(my_pos: Position, my_precesion: float, distance_to_target: float, enemy_positions: List[Position]) ->  Tuple[float, float, float]:
    command = 0
    pitch = 0
    precesion = 0
    if len(enemy_positions) >= 2:
        curr_pos = enemy_positions[len(enemy_positions)- 1]
        prev_pos = enemy_positions[len(enemy_positions)- 2]
        relative_pos = Position(x=curr_pos.x - prev_pos.x, y=0, z=curr_pos.z - prev_pos.z)
        future_pos = Position(x=curr_pos.x + relative_pos.x, y=0, z=curr_pos.z + relative_pos.z)

        desired_precesion = np.rad2deg(
            math.atan2(future_pos.z, future_pos.x) - math.pi / 2
        )
        precesion_error = desired_precesion - my_precesion
        precesion_error = mod((precesion_error + 180), 360) - 180
        print(f"precesion_error: {precesion_error}")
    # If in target range
    if distance_to_target < 3200:
        if is_in_safe_zone(my_pos):
            command = 11
        pitch = 10
        if distance_to_target > 2600 and distance_to_target < 3000:
            pitch = 8
        if distance_to_target > 2200 and distance_to_target < 2600:
            pitch = 5
        if distance_to_target > 2000 and distance_to_target < 2200:
            pitch = 3
        if distance_to_target > 1500 and distance_to_target < 2000:
            pitch = 1.5
        if distance_to_target < 1500:
            pitch = 0
    return command, pitch, precesion