import socket
from struct import pack

from src.models.command_order import CommandOrder


class ControllerService:
    def __init__(self, ip_address, port, pack_code="iffffffiLiiifffi?i"):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server_address = (str(ip_address), int(port))
        self.__pack_code = pack_code

    def send_command(self, cmd: CommandOrder):
        data = pack(
            self.__pack_code,
            cmd.controlling_id,
            cmd.thrust,
            cmd.roll,
            cmd.pitch,
            cmd.yaw,
            cmd.precesion,
            cmd.bank,
            cmd.faction,
            cmd.timer,
            cmd.command,
            cmd.spawnid,
            cmd.type_of_island,
            cmd.x,
            cmd.y,
            cmd.z,
            cmd.target,
            cmd.bit,
            cmd.weapon,
        )
        return self._socket.sendto(data, self.__server_address)
