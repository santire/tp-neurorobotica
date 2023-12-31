import socket
import numpy as np
from threading import Thread
from struct import unpack

from src.models.telemetry_info import TelemetryInfo
from src.models.position import Position


_td = {
    "timer": 0,
    "number": 1,
    "health": 2,
    "power": 3,
    "bearing": 4,
    "x": 5,
    "y": 6,
    "z": 7,
    "R1": 8,
    "R2": 9,
    "R3": 10,
    "R4": 11,
    "R5": 12,
    "R6": 13,
    "R7": 14,
    "R8": 15,
    "R9": 16,
    "R10": 17,
    "R11": 18,
    "R12": 19,
}


class TelemetryService(Thread):
    def __init__(
        self,
        ip_address,
        port,
        packet_length=84,
        unpack_code="Liiiffffffffffffffff",
    ):
        Thread.__init__(self)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((str(ip_address), int(port)))
        self.__packet_length = packet_length
        self.__unpack_code = unpack_code
        self.__entities_info = {}
        # Daemon thread stops when program exits
        self.daemon = True
        self.start()

    def run(self):
        # Constantly poll from socket, storing latest info on
        # map based on telemetry number
        while True:
            tel_info = self._poll()
            self.__entities_info[tel_info.number] = tel_info

    def poll(self, tank_number) -> TelemetryInfo:
        # Get latest telemetry info of given number
        return self.__entities_info.get(tank_number, None)

    def _poll(self) -> TelemetryInfo:
        data, _ = self._socket.recvfrom(self.__packet_length)
        if len(data) != self.__packet_length:
            raise Exception(
                f"Received invalid packet size. Expected: {self.__packet_length}, got: {len(data)}"
            )

        values = unpack(self.__unpack_code, data)

        def get(x):
            return values[_td[x]]

        rot_matrix = np.matrix(np.array(values[_td["R1"]:]).reshape(4, 3))
        tel_info = TelemetryInfo(
            timer=get("timer"),
            number=get("number"),
            health=get("health"),
            power=get("power"),
            bearing=get("bearing"),
            body_pos=Position(x=get("x"), y=get("y"), z=get("z")),
            body_rot=rot_matrix,
        )
        return tel_info
