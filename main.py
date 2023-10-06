import os

from src.services.telemetry_service import TelemetryService

IP = os.getenv("TANK_TELEMETRY_IP")
PORT = os.getenv("TANK_TELEMETRY_PORT")
telemetry_service = TelemetryService(IP, PORT)

i = 0
while True:
    tel_info = telemetry_service.poll(tank_number=1)
    if i % 100 == 0:
        print(tel_info)
    i += 1
