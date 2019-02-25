from typing import List, Dict, Tuple, Any

import dynamixel_sdk as sdk

from . import util
from .motor import Motor, MotorType
from .register import Instruction
from .connection import Connection
from .register import AX, MX


class MotorChain:
    def __init__(
        self, conn: Connection, initial: List[Motor] = [], protocol_v: float = 1.0
    ):
        self.homogenous = True
        self.motors = initial
        self._update_homogenous()
        self.conn = conn
        self.packet_handler = sdk.PacketHandler(protocol_v)

    def add_one_motor(self, m: Motor) -> None:
        self.motors.append(m)

    def add_motors(self, m: List[Motor]) -> None:
        self.motors.extend(m)

    def _update_homogenous(self) -> None:
        self.homogenous = len(set(m.protocol_version for m in self.motors)) == 1

    def write_one_motor(
        self, instruction: Instruction, id: int, val: int
    ) -> Tuple[Any, Any]:
        for m in self.motors:
            if m.id == id:
                return m.write(instruction, val)
        raise RuntimeError(f"Motor id {id} not found for write_one_motor")

    def write_one_value(self, instruction: Instruction, vals: int) -> bool:
        # if self.homogenous:
        pass

    def write_many_values(self, instruction: Instruction, vals: Dict[int, int]) -> bool:
        if self.homogenous:
            chain_type = self.motors[0].type
            table = AX if chain_type == MotorType.AX else MX
            addrs = table[instruction]
            pos, size = min(addrs), len(addrs)
            groupSyncWrite = sdk.GroupSyncWrite(
                self.conn.port_handler, self.packet_handler, pos, size
            )
            for k, v in vals.items():
                if size == 2:
                    dxl_addparam_result = groupSyncWrite.addParam(
                        k, util.create2ByteArray(v)
                    )
                else:
                    dxl_addparam_result = groupSyncWrite.addParam(
                        k, util.create1ByteArray(v)
                    )
                assert dxl_addparam_result, "Group Sync Write Failed"
            dxl_comm_result = groupSyncWrite.txPacket()
            return dxl_comm_result
        else:
            raise NotImplementedError("Bulk write not implemented")
