import math
import os
import sys
import time
import numpy as np
from dotenv import load_dotenv
from src.models.command_order import CommandOrder
from src.models.position import Position
from src.services.controller_service import ControllerService
from src.services.telemetry_service import TelemetryService

load_dotenv()

CONTROL_IP = os.getenv("TANK_CONTROL_IP")
CONTROL_PORT = os.getenv("TANK_CONTROL_PORT")
TELEMETRY_IP = os.getenv("TANK_TELEMETRY_IP")
TELEMETRY_PORT = os.getenv("TANK_TELEMETRY_PORT")

telemetry_service = TelemetryService(TELEMETRY_IP, TELEMETRY_PORT)
controller_service = ControllerService(CONTROL_IP, CONTROL_PORT)


cmd = CommandOrder(
    controlling_id=1,
    thrust=0,
    roll=0,
    pitch=0,
    timer=-1,
    precesion=0,
    command=0,
    x=0,
    z=0,
)

old_tel_info = None

rotation_gain = 0.1
thrust_gain = 0.05

max_thrust = 200
max_rotation = 20

first_start = time.time()
start = time.time()

while True:
    my_tel_info = telemetry_service.poll(tank_number=1)
    enemy_tel_info = telemetry_service.poll(tank_number=2)
    current_time = time.time()

    def mod(a, n):
        return (a % n + n) % n

    if current_time - start <= 0.2:
        continue
    elif (
        my_tel_info is not None
        and enemy_tel_info is not None
        and my_tel_info != old_tel_info
    ):
        old_tel_info = my_tel_info
        start = current_time
        my_pos = my_tel_info.body_pos
        my_bearing = my_tel_info.bearing
        enemy_pos = enemy_tel_info.body_pos

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
        if enemy_tel_info.health < 1000:
            print(f"hit at: {distance_to_target}")
        if enemy_tel_info.health <= 0:
            print(f"Final hit at: {distance_to_target}")
            print(f"Elapsed time: {time.time()-first_start}")
            sys.exit(0)

        if distance_to_target < 3200:
            cmd.command = 11
            cmd.pitch = 10
            if distance_to_target > 2600 and distance_to_target < 3000:
                cmd.pitch = 8
            if distance_to_target > 2200 and distance_to_target < 2600:
                cmd.pitch = 5
            if distance_to_target > 2000 and distance_to_target < 2200:
                cmd.pitch = 3
            if distance_to_target > 1500 and distance_to_target < 2000:
                cmd.pitch = 1.5
            if distance_to_target < 1500:
                cmd.pitch = 0

        cmd.timer = my_tel_info.timer + 1
        cmd.thrust = thrust
        cmd.roll = roll
        controller_service.send_command(cmd)
