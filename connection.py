import dynamixel_sdk as sdk


class Connection:
    def __init__(self, port):
        self.port = port
        self.port_handler = sdk.PortHandler(port)
