import dynamixel_sdk as sdk


class Connection:
    def __init__(self, port: str, baudrate: int = 1_000_000):
        self.port = port
        self.port_handler = sdk.PortHandler(port)
        self.baudrate = baudrate
        self.opened = False

    def open_port(self) -> bool:
        ret = self.port_handler.openPort()
        self.opened = ret
        return ret

    def set_baud_rate(self, baud_rate: int) -> bool:
        ret = self.port_handler.setBaudRate(self.baudrate)
        self.opened = ret
        return ret
