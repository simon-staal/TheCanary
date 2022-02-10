import smbus2
import struct
from time import sleep
import math

"""
Interface fo BMP280
Datasheet: https://cdn-shop.adafruit.com/datasheets/BST-BMP280-DS001-11.pdf
"""

""" Parameter options, use these to update the value of relevant parameters"""
CHIP_ID = 0x58
RESET = 0xB6

# Mode values
SLEEP_MODE = 0 # I sleep
FORCE_MODE = 0x01 # Real shit? (allows us to force a measurement, returns to sleep after)
NORMAL_MODE = 0x03 # Takes measurements regularly

_MODES = (SLEEP_MODE, FORCE_MODE, NORMAL_MODE) # Enum, used for value checking

# Oversampling values (for both temperature and pressure), higher values -> increase resolution + reduce noise
# Increases power consumption (obv)
# It is recommended to set the temperature oversampling to x2 (or less if pressure is sampled less)
DISABLED = 0 # Skips measurement
OVERSAMPLE_X1 = 0x01
OVERSAMPLE_X2 = 0x02
OVERSAMPLE_X4 = 0x03
OVERSAMPLE_X8 = 0x04
OVERSAMPLE_X16 = 0x05

_OVERSAMPLE = (DISABLED, OVERSAMPLE_X1, OVERSAMPLE_X2, OVERSAMPLE_X4, OVERSAMPLE_X8, OVERSAMPLE_X16)

# Standby time values (in ms), defines how often measurements are taken in normal mode (kinda, see datasheet)
STANDBY_0_5 = 0
STANDBY_62_5 = 0x1
STANDBY_125 = 0x2
STANDBY_250 = 0x3
STANDBY_500 = 0x4
STANDBY_1000 = 0x5
STANDBY_2000 = 0x6
STANDBY_4000 = 0x7

_STANDBY = (STANDBY_0_5, STANDBY_62_5, STANDBY_125, STANDBY_250, STANDBY_500, STANDBY_1000, STANDBY_2000, STANDBY_4000)

# iir filter values, used to suppress disturbances in output data 
IIR_DISABLE = 0
IIR_X2 = 0x01
IIR_X4 = 0x02
IIR_X8 = 0x03
IIR_X16 = 0x04

_IIR_FILTER = (IIR_DISABLE, IIR_X2, IIR_X4, IIR_X8, IIR_X16)


"""Slave register addresses - ignore this"""
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

"""
Anything marked by @property can be accessed like a member variable.
e.g.
bus = smbus2.SMBus(1)
sensor = SENSOR(bus)

temp = sensor.temperature // Gets temperature from sensor
sensor.mode = SLEEP_MODE // Sets mode to SLEEP

Everything is managed internally, any variable prefixed with an '_' is private and should not be touched.

The rate at which measurements can be performed depends on the mode / oversampling parameters. Refer to 3.8.1 and 3.8.2 of the datasheet

Using default initialisation values, can read every 100ms (should be fast enough)
"""
class SENSOR():
    def __init__(self, bus):
        self._addr = 0x77
        self._regs = SENSOR_REGISTERS()
        self.bus = bus

        # Default values (handheld device low-power mode defined in table 15 of datasheet)
        self._mode = SLEEP_MODE
        self._oversample_temperature = OVERSAMPLE_X2
        self._oversample_pressure = OVERSAMPLE_X16
        self._t_standby = STANDBY_62_5
        self._iir_filter = IIR_X4

        chip_id = self._read_byte(self.regs.id)
        assert chip_id == CHIP_ID, print(f'ERROR: Failed to find BPM280, Chip ID = {chip_id}')

        self._reset()
        self._read_compensation()
        self._write_ctrl_meas()
        self._write_config()

        self._t_fine = None
        self.sea_level_pressure = 1013.25 # Pressure in hPa at sea level


    """ PUBLIC STUFF -- USE THIS"""

    """Controls sensor mode, valid values are listed above in constants"""
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        assert value in _MODES, print(f"ERROR: Invalid mode {value}")

        self._mode = value
        self._write_ctrl_meas()

    """Controls sensor measurement standy period"""
    @property
    def standby(self):
        return self._t_standby

    @standby.setter
    def standby(self, value):
        assert value in _STANDBY, print(f'ERROR: Invalid standby period {value}')

        if self._t_standby == value:
            return
        
        self._t_standby = value
        self._write_config()

    """Controls sensor temperature oversampling coefficient"""
    @property
    def oversample_temperature(self):
        return self._oversample_temperature

    @oversample_temperature.setter
    def oversample_temperature(self, value):
        assert value in _OVERSAMPLE, print(f'ERROR: Invalid temperature oversampling value {value}')

        self._oversample_temperature = value
        self._write_ctrl_meas()

    """Controls sensor pressure oversampling coefficient"""
    @property
    def oversample_pressure(self):
        return self._oversample_pressure

    @oversample_pressure.setter
    def oversample_pressure(self, value):
        assert value in _OVERSAMPLE, print(f'ERROR: Invalid pressure oversampling value {value}')

        self._oversample_pressure = value
        self._write_ctrl_meas()

    """IIR filter coefficient, see constants"""
    @property
    def iir_filter(self):
        return self._iir_filter

    @iir_filter.setter
    def iir_filter(self, value):
        assert value in _IIR_FILTER, print(f'ERROR: Invalid IIR Filter value {value}')

        self._iir_filter = value
        self._write_config()

    """Compensated temperature in degrees Celsius"""
    @property
    def temperature(self):
        self._read_t_fine()
        return self._t_fine / 5120.0

    """Compensated pressure in hectoPascals (hPa)"""
    @property
    def pressure(self):
        self._read_t_fine()

        # Datasheet algorithm (that's why variable names suck)
        # Also I have no idea what's going on here lol
        # Made everything floats to make life simpler, if this tanks performance I'll re-implement using bit manip stuff
        # Remeber that premature optimization is the root of all evil
        adc = self._read20(self._regs.pressure)
        var1 = self._t_fine / 2.0 - 64000.0
        var2 = var1 ** 2 * self._pressure_comp[5] / 32768.0
        var2 += var1 * self._pressure_comp[4] * 2.0
        var2 = var2 / 4.0 + self._pressure_comp[3] * 65536.0
        var3 = self._pressure_comp[2] * var1 ** 2 / 524288.0
        var1 = (var3 + self._pressure_comp[1] * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self._pressure_comp[0]
        
        # Avoid divide by 0 error
        assert var1, print("ERROR: Failed to calculate pressure, possible error while reading compensation registers")

        pressure = 1048576.0 - adc
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = self._pressure_comp[8] * pressure ** 2 / 2147483648.0
        var2 = pressure * self._pressure_comp[7] / 32768.0
        pressure += (var1 + var2 + self._pressure_comp[6]) / 16.0
        
        return pressure / 100

    """Altitude based on sea level pressure, update sea_level_pressure as needed. No clue if this will be reliable underground XD -- i'm sure it is"""
    @property
    def altitude(self):
        p = self.pressure
        return 44330 * (1.0 - math.pow(p / self.sea_level_pressure, 0.1903))

    """ PRIVATE STUFF -- NO TOUCHY >:( """
    def _read_byte(self, register):
        return self.bus.read_byte_data(self._addr, register)

    def _read_register(self, register, bytes):
        return self.bus.read_i2c_block_data(self._addr, register, bytes)

    def _write_byte(self, register, data):
        self.bus.write_byte_data(self._addr, register, data)

    def _reset(self):
        self._write_byte(self._regs.reset, RESET)
        sleep(0.005)

    def _get_status(self):
        return self._read_byte(self._regs.status)

    def _read_compensation(self):
        coeff = self._read_register(self._regs.compensation, 24)
        coeff = struct.unpack("<HhhHhhhhhhhh", bytes(coeff)) # Unpack bytes as per datasheet (looks funny lol)
        coeff = [float(i) for i in coeff]
        self._temp_comp = coeff[:3]
        self._pressure_comp = coeff[3:]
        
    @property
    def _ctrl_meas(self):
        ctrl_meas = self._oversample_temperature << 5
        ctrl_meas += self._oversample_pressure << 2
        ctrl_meas += self._mode
        return ctrl_meas

    def _write_ctrl_meas(self):
        self._write_byte(self._regs.ctrl_meas, self._ctrl_meas)

    @property
    def _config(self):
        config = 0
        if self.mode == NORMAL_MODE:
            config += self._t_standby << 5
        if self._iir_filter:
            config += self._iir_filter << 2
        return config

    def _read_config(self):
        return self._read_byte(self._regs.config)

    def _write_config(self):
        normalMode = False
        # Writes to config are ignored in normal mode
        if self._mode == NORMAL_MODE:
            normalMode = True
            self.mode = SLEEP_MODE
        self._write_byte(self._regs.config, self._config)

        # Reset mode if switched to sleep
        if normalMode:
            self.mode = NORMAL_MODE

    """Used to read temperature / pressure values from registers (this device is so fkn weird), returns a float"""
    def _read20(self, register):
        ret = 0.0
        vals = self._read_register(register, 3)
        vals[2] = vals[2] >> 4
        for b in vals:
            ret *= 256.0
            ret += float(b & 0xFF)
        return ret

    def _read_t_fine(self):
        # We need to take measurement ourselves
        if self.mode != NORMAL_MODE:
            self.mode = FORCE_MODE
            while getBit(self._get_status(), 3):
                sleep(0.002)
        
        raw_temperature = self._read20(self._regs.temperature)
        # Allow the names, copied from datasheet algorithm
        var1 = (raw_temperature / 16384.0 - self._temp_comp[0] / 1024.0) * self._temp_comp[1]
        var2 = (
            (raw_temperature / 131072.0 - self._temp_comp[0] / 8192.0) ** 2) * self._temp_comp[2]

        self._t_fine = var1 + var2

# Helper function to isolate a bit of a given byte
def getBit(val, idx):
    return (val & (1 << idx)) >> idx