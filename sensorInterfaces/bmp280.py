import smbus2
import struct
from time import sleep

# Helper function to isolate a bit of a given byte
def getBit(val, idx):
    return (val & (1 << idx)) >> idx

# Slave register addresses
class SENSOR_REGISTERS():
    # Contains chip identification number == 0x58. Can be read as soon as device finished power-on-reset
    id = 0xD0 # R

    # If the value 0xB6 is written to the register the device is reset using complete power-on-reset procedure
    reset = 0xE0 # W

    # Status of the device
    status = 0xF3 # R

    # Sets data acquisition options of the device
    ctrl_meas = 0xF4 # R/W

    # Sets rate, filter and interface options of device
    config = 0xF5 # R/W

    # 3 bytes, contains raw pressure measurement output data
    pressure = 0xF7

    # 3 bytes, contains raw temperature measurement output data
    temperature = 0xFA

    # 24 bytes, contains compensation parameters to calibrate temperature and pressure readings
    compensation = 0x88

CHIP_ID = 0x58
RESET = 0xB6

# Mode values
SLEEP_MODE = 0
FORCE_MODE = 0x01
NORMAL_MODE = 0x03

# Oversampling values, higher values -> increase resolution + reduce noise
# It is recommended to set the temperature oversampling to x2 (or less if pressure is sampled less)
DISABLED = 0 # Skips measurement
OVERSAMPLE_X1 = 0x01
OVERSAMPLE_X2 = 0x02
OVERSAMPLE_X4 = 0x03
OVERSAMPLE_X8 = 0x04
OVERSAMPLE_X16 = 0x05

class SENSOR():
    def __init__(self, bus):
        self._addr = 0x77
        self._regs = SENSOR_REGISTERS()
        self.bus = bus
        self._mode = SLEEP_MODE
        self._oversample_temperature = OVERSAMPLE_X2
        self._oversample_pressure = OVERSAMPLE_X16

        chip_id = self._read_byte(self.regs.id)
        assert chip_id == CHIP_ID, print(f'ERROR: Failed to find BPM280, Chip ID = {chip_id}')

        self._reset()
        self._read_compensation()
        self._write_ctrl_meas()


    def _read_byte(self, register):
        return self.bus.read_byte_data(self._addr, register)

    def _read_register(self, register, bytes):
        return self.bus.read_i2c_block_data(self._addr, register, bytes)

    def _write_byte(self, register, data):
        self.bus.write_byte_data(self._addr, register, data)

    def _reset(self):
        self._write_byte(self._regs.reset, RESET)
        sleep(0.005)

    def _read_compensation(self):
        coeff = self._read_register(self._regs.compensation, 24)
        coeff = struct.unpack("<HhhHhhhhhhhh", bytes(coeff))

    @property
    def _ctrl_meas(self):
        ctrl_meas = self._oversample_temperature << 5
        ctrl_meas += self._oversample_pressure << 2
        ctrl_meas += self._mode
        return ctrl_meas

    def _write_ctrl_meas(self):
        self._write_byte(self._regs.ctrl_meas, self._ctrl_meas)

    def setMode(self, mode)

def read24(res):
    """Read an unsigned 24-bit value as a floating point and return it."""
    ret = 0.0
    for b in res:
        ret *= 256.0
        ret += float(b & 0xFF)
    return ret