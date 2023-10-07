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
from src.services.combat_service import *

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

enemy_pos_list = []
last_enemy_health = 1000


while True:

    my_tel_info = telemetry_service.poll(tank_number=1)
    enemy_tel_info = telemetry_service.poll(tank_number=2)

    current_time = time.time()

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

        if not is_in_safe_zone(my_pos):
            enemy_pos = Position(x=0, y=0, z=0)

        thrust, roll, distance_to_target = get_tank_params(my_bearing=my_bearing, my_pos=my_pos, enemy_pos=enemy_pos)

        enemy_pos_list.append(Position(x=enemy_pos.x, y=0, z=enemy_pos.z))
        command, pitch, precesion = get_turret_params(my_pos=my_pos, distance_to_target=distance_to_target, enemy_positions=enemy_pos_list)
        
        if enemy_tel_info.health < last_enemy_health:
            print(f"hit at: {distance_to_target}")
        last_enemy_health = enemy_tel_info.health
        if enemy_tel_info.health <= 0:
            print(f"Final hit at: {distance_to_target}")
            print(f"Elapsed time: {time.time()-first_start}")
            sys.exit(0)

        cmd.timer = my_tel_info.timer + 1
        cmd.thrust = thrust
        cmd.roll = roll
        cmd.pitch = pitch
        cmd.precesion = precesion
        cmd.command = command
        print('antes sendo command')
        controller_service.send_command(cmd)


# TODO

# 1. DONE Que no se muera con el agua (Trate de sobrevivir)
# 2. No disparar a menos heading_error (de la torreta) < ERROR (ponele 5 grados)
# tldr: instinto de supervivencia y apuntar para disparar
