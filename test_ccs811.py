import smbus2

# Helper function to isolate a bit of a given byte
def getBit(val, idx):
    return (val & (1 << idx)) >> idx

# Slave register addresses
class SENSOR_REGISTERS():
    STATUS = 0x00 # R
    MODE = 0x01 # R/W

    # The most signifcant 2 bytes contain a ppm estimate of eCO2 level, next 2 bytes contain a ppg estimate of the total VOC level
    ALG_RESULT_DATA = 0x02 # R

    # Temperature / humidity data can be written to enable compensation
    ENV_DATA = 0x05 # W

    # Error source location
    ERROR_ID = 0xE0 # R

    # Used to launch application
    APP_START = 0xF4 # W
# Sensor class
class SENSOR():
    # Sensor parameters, change depending on your sensor
    ADDR = 0x5A # Can be 0x5B, check I2C connection
    REGS = SENSOR_REGISTERS()

    def __init__(self, bus, addr=0x5A, regs=SENSOR_REGISTERS()):
        self.ADDR = addr
        self.REGS = regs
        self.bus = bus
        self.status = self.bus.read_byte_data(self.ADDR, self.REGS.STATUS)
        self.mode = self.bus.read_byte_data(self.ADDR, self.REGS.MODE)
        self.printStatus()

    def updateStatus(self, bus):
        self.status = bus.read_byte_data(self.ADDR, self.REGS.STATUS)

    def startApp(self):
        self.bus.write_i2c_block_data(self.ADDR, self.REGS.APP_START, [])
    
    def printStatus(self):
        status = self.status
        FW_MODE = getBit(status, 7)
        print(f'FW_MODE: {FW_MODE}')
        if FW_MODE == 0: 
            print("Sensor is in boot mode")
            print("Starting application")
            self.startApp()
            print("Please get new status")
            return
        APP_VALID = getBit(status, 4)
        print(f'APP_VALID: {APP_VALID}')
        assert APP_VALID == 1, "ERROR: Sensor does not have valid application firmware"
        DATA_READY = getBit(status, 3)
        print(f'DATA_READY: {DATA_READY}')
        ERROR = getBit(status, 0)
        print(f'ERROR: {ERROR}')
        if DATA_READY == 1: print('Data is ready to be read')
        if ERROR == 1: print('Read ERROR_ID')

    def newData(self):
        return getBit(self.status, 3)

    def getCO2(self):
        co2 = self.bus.read_i2c_block_data(self.ADDR, self.REGS.ALG_RESULT_DATA, 2)
        print(type(co2))
        print(co2)
        #return int.from_bytes(read_result.buf[0]+read_result.buf[1],’big’)



""" Deal with these values later
# Slave register read values
DEVICE_STATE_BOOT = 0x10
DEVICE_STATE_APP = 0x90
DEVICE_STATE_APP_WITH_DATA = 0x98

# Slave register write values
DEVICE_SET_MODE_10S = [0x10]
DEVICE_SET_SW_RESET = [0x11, 0xE5, 0x72, 0x8A]
"""

bus = smbus2.SMBus(1)
sensor = SENSOR(bus)

