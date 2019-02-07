import dynamixel_sdk as sdk
from typing import Union, Tuple, Any
from enum import Enum

from .connection import Connection
from .register import Instruction, AX, MX
from .util import validate_response


class MotorType(Enum):
    AX = 1
    MX = 2


class Motor:
    def __init__(
        self, conn: Connection, id: int, type: MotorType, protocol_ver: float = 1.0
    ):
        self.id = id
        self.type = type
        self.conn = conn
        self.protocol_version = protocol_ver
        self.packet_handler = sdk.PacketHandler(self.protocol_version)
        self.regtable = AX if self.type == MotorType.AX else MX

    def write(self, instruction: Instruction, value: int) -> Tuple[Any, Any]:
        addrs = self.regtable[instruction]
        start, width = min(addrs), len(addrs)
        try:
            return {
                1: self.packet_handler.write1ByteTxRx,
                2: self.packet_handler.write2ByteTxRx,
                4: self.packet_handler.write4ByteTxRx,
            }[width](self.conn.port_handler, self.id, start, value)
        except KeyError:
            raise NotImplementedError(f"Register width not supported {width}")

    def read(self, instruction: Instruction) -> int:
        addrs = self.regtable[instruction]
        start, width = min(addrs), len(addrs)
        try:
            return {
                1: self.packet_handler.read1ByteTxRx,
                2: self.packet_handler.read2ByteTxRx,
                4: self.packet_handler.read4ByteTxRx,
            }[width](self.conn.port_handler, self.id, start)
        except KeyError:
            raise NotImplementedError(f"Register width not supported {width}")
