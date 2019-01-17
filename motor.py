import dynamixel_sdk as dxl
import logging
from time import sleep

import control_table


def constrain(val, lo, hi):
    """Constrains `val` to the range [lo, hi]"""
    if val < lo:
        return lo
    elif val > hi:
        return hi
    return val


class Motor:

    BAUDRATE = 1_000_000
    PROTOCOL_VERSION = 1.0
    opened = False

    def __init__(self, id, port, type="AX"):
        self.portHandler = dxl.PortHandler(port)
        self.packetHandler = dxl.PacketHandler(self.PROTOCOL_VERSION)
        self.id = id
        self.port = port
        self.ctrl = control_table.ControlTable(type)
        self.type = type

        if self.portHandler.openPort():
            logging.info(f"Motor#{id} opened on port #{port}")
            self.opened = True
        else:
            logging.error(f"Motor #{id} failed to open on port #{port}")

        self._set_baud_rate()

    def _set_baud_rate(self):
        if not self.portHandler.setBaudRate(self.BAUDRATE):
            logging.error(f"setBaudRate failed on Motor #{id} - Port #{self.port}")
            self.opened = False

    def _validate_response(self, res, err):
        if res != dxl.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(res))
        elif err != 0:
            print("%s" % self.packetHandler.getRxPacketError(err))
        else:
            return True
        self.opened = False
        return False

    def set_torque(self, val: bool):
        res, err = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            self.id,
            self.ctrl.regnum("TORQUE_ENABLE"),
            1 if val else 0,
        )
        self._validate_response(res, err)

    def move(self, pos):
        pos = constrain(pos, 0, 1023)
        res, err = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.id, self.ctrl.regnum("GOAL_POSITION"), pos
        )
        self._validate_response(res, err)

    def get_current_position(self):
        pos, res, err = self.packetHandler.read4ByteTxRx(
            self.portHandler, self.id, self.ctrl.regnum("CURRENT_POSITION")
        )
        self._validate_response(res, err)
        return pos

    def set_speed(self, pos):
        pos = constrain(pos, 0, 1023)
        res, err = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.id, self.ctrl.regnum("MOVING_SPEED"), pos
        )
        self._validate_response(res, err)


if __name__ == "__main__":
    m = Motor(4, "/dev/cu.usbserial-A5052NHF")
    m._set_baud_rate()
    m.set_speed(300)
    m.move(512)
