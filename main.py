import os
import time

from src.services.telemetry_service import TelemetryService

IP = os.getenv("TANK_TELEMETRY_IP")
PORT = os.getenv("TANK_TELEMETRY_PORT")
telemetry_service = TelemetryService(IP, PORT)

old_tel_info = None
start = time.time()
while True:
    current_time = time.time()
    tel_info = telemetry_service.poll(tank_number=1)
    if current_time - start >= 1 and tel_info != old_tel_info:
        print(tel_info)
        start = current_time
    old_tel_info = tel_info
