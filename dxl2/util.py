import dynamixel_sdk as sdk

from dynamixel_sdk import DXL_LOBYTE, DXL_LOWORD, DXL_HIBYTE, DXL_HIWORD


def validate_response(packet_handler, res, err):
    if res != sdk.COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(res))
    elif err != 0:
        print("%s" % packet_handler.getRxPacketError(err))
    else:
        return True
    return False


def create2ByteArray(bin_value):
    byte_array = [DXL_LOBYTE(DXL_LOWORD(bin_value)), DXL_HIBYTE(DXL_LOWORD(bin_value))]
    return byte_array


def create1ByteArray(bin_value):
    byte_array = [DXL_LOBYTE(DXL_LOWORD(bin_value))]
    return byte_array
