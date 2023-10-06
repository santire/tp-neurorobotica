import os
import time
from dotenv import load_dotenv
from src.models.command_order import CommandOrder
from src.services.controller_service import ControllerService
from src.services.telemetry_service import TelemetryService

load_dotenv()

CONTROL_IP = os.getenv("TANK_CONTROL_IP")
CONTROL_PORT = os.getenv("TANK_CONTROL_PORT")
TELEMETRY_IP = os.getenv("TANK_TELEMETRY_IP")
TELEMETRY_PORT = os.getenv("TANK_TELEMETRY_PORT")

telemetry_service = TelemetryService(TELEMETRY_IP, TELEMETRY_PORT)
controller_service = ControllerService(CONTROL_IP, CONTROL_PORT)

shoot_cmd = CommandOrder(
    controlling_id=1,
    thrust=0,
    roll=0,
    pitch=0,
    timer=-1,
    precesion=0,
    command=11,
    x=0,
    z=0,
)

old_tel_info = None
start = time.time()
shoot_start = time.time()
shoot_end = shoot_start + 0.5
shooting = False
while True:
    current_time = time.time()
    tel_info = telemetry_service.poll(tank_number=1)
    if current_time - start >= 1 and tel_info != old_tel_info:
        start = current_time
    old_tel_info = tel_info

    if tel_info is not None:
        # Start shooting every 10 seconds
        if current_time - shoot_start >= 2:
            print("Firing burst")
            if shooting is False:
                shoot_cmd.timer = tel_info.timer + 1
                shoot_cmd.command = 11
                controller_service.send_command(shoot_cmd)
                shoot_start = current_time
                shooting = True

        # Stop shooting half a second later
        if current_time - shoot_end >= 0.5:
            if shooting is True:
                shooting = False
                shoot_cmd.timer = tel_info.timer + 1
                shoot_cmd.command = 0
                controller_service.send_command(shoot_cmd)
                shoot_end = shoot_start + 0.5
