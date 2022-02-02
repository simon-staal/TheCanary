from asyncio.windows_events import NULL
import smbus2
from time import sleep

# Slave register addresses
class SENSOR_REGISTERS():
    STATUS = 0x00 # R
    MEAS_MODE = 0x01 # R/W

    # The most signifcant 2 bytes contain a ppm estimate of eCO2 level, next 2 bytes contain a ppg estimate of the total VOC level
    ALG_RESULT_DATA = 0x02 # R

    # Temperature / humidity data can be written to enable compensation
    ENV_DATA = 0x05 # W

    # Error source location
    ERROR_ID = 0xE0 # R

class SENSOR():
    ADDR = 0x5A # Can be 0x5B, check I2C connection
    REGS = SENSOR_REGISTERS()

    def __init__(self, bus):
        self.bus = bus
        self.status = self.bus.read_byte_data(self.ADDR, self.REGS.STATUS)

    def updateStatus(self, bus):
        self.status = bus.read_byte_data(self.ADDR, self.REGS.STATUS)

    def print_status(self):
        status = self.status
        FW_MODE = getBit(status, 7)
        print(f'FW_MODE: {FW_MODE}')
        assert FW_MODE == 1, "ERROR: Sensor is in boot mode"
        APP_VALID = getBit(status, 4)
        print(f'APP_VALID: {APP_VALID}')
        assert APP_VALID == 1, "ERROR: Sensor does not have valid application firmware"
        DATA_READY = getBit(status, 3)
        print(f'DATA_READY: {DATA_READY}')
        ERROR = getBit(status, 0)
        print(f'ERROR: {ERROR}')
        if DATA_READY == 1: print('Data is ready to be read')
        if ERROR == 1: print('Read ERROR_ID')


def getBit(val, idx):
    return (val & (1 << idx)) >> idx

def new_data(status):
    getBit(status, 3)

""" Deal with these values later
# Slave register read values
DEVICE_STATE_BOOT = 0x10
DEVICE_STATE_APP = 0x90
DEVICE_STATE_APP_WITH_DATA = 0x98

# Slave register write values
DEVICE_SET_MODE_10S = [0x10]
DEVICE_SET_SW_RESET = [0x11, 0xE5, 0x72, 0x8A]
"""

# Run this function
def startup(bus, device):
    status = bus.read_byte_data(device.ADDR, device.REGS.STATUS)
    device.print_status(status)

# I2C Bus
bus = smbus2.SMBus(1)
sensor = SENSOR(bus)