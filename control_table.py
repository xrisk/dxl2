ax = {
    "TORQUE_ENABLE": [24, 1],
    "CURRENT_POSITION": [132, 4],
    "GOAL_POSITION": [30, 2],
    "MOVING_SPEED": [32, 2],
}


class ControlTable:
    def __init__(self, mtype):
        self.mtype = mtype

    def regnum(self, regname):
        if self.mtype == "AX":
            return ax[regname][0]

    def bytes(self, regname):
        if self.mtype == "AX":
            return ax[regname][1]
