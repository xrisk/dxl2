import dynamixel_sdk as sdk
from connection import Connection
from register import Instruction, AX, MX
from typing import Union
from enum import Enum


class MotorType(Enum):
    AX = 1
    MX = 1


class Motor:
    def __init__(self, id: int, type: MotorType, conn: Connection, protocol_ver: int):
        self.id = id
        self.type = type
        self.conn = conn
        self.protocol_version = protocol_ver
        self.packet_handler = sdk.PacketHandler(self.protocol_version)

    def write(self, instruction: Instruction, value: int):
        if self.type == MotorType.AX:
            addr, l = AX.get(instruction)
        elif self.type == MotorType.MX:
            addr, l = MX.get(instruction)
        else:
            raise Exception("Unsupported Motor type {}")

        if l == 1:
            self.packet_handler.write1ByteTxRx(
                self.conn.port_handler, self.id, addr, value
            )
        elif l == 2:
            self.packet_handler.write2ByteTxRx(
                self.conn.port_handler, self.id, addr, value
            )
        elif l == 4:
            self.packet_handler.write4ByteTxRx(
                self.conn.port_handler, self.id, addr, value
            )

    def read(self, instruction: Instruction) -> int:
        if self.type == MotorType.AX:
            addr, l = AX.get(instruction)
        elif self.type == MotorType.MX:
            addr, l = MX.get(instruction)
        else:
            raise Exception("Unsupported Motor type {}")

        if l == 1:
            self.packet_handler.read1ByteTxRx(self.conn.port_handler, self.id, addr)
        elif l == 2:
            self.packet_handler.read2ByteTxRx(self.conn.port_handler, self.id, addr)
        elif l == 4:
            self.packet_handler.read4ByteTxRx(self.conn.port_handler, self.id, addr)
