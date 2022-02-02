import smbus2
from time import sleep

# Helper function to isolate a bit of a given byte
def getBit(val, idx):
    return (val & (1 << idx)) >> idx

def bitStringToByte(bitstring):
        return int(bitstring, 2) & 0xFF

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

    def __init__(self, addr, regs, bus):
        self.ADDR = addr
        self.REGS = regs
        self.bus = bus
        self.status = self.bus.read_byte_data(self.ADDR, self.REGS.STATUS)
        self.mode = self.bus.read_byte_data(self.ADDR, self.REGS.MODE)
        self.printStatus()

    def updateStatus(self, bus):
        self.status = bus.read_byte_data(self.ADDR, self.REGS.STATUS)
        self.printStatus()

    def startApp(self):
        self.bus.write_i2c_block_data(self.ADDR, self.REGS.APP_START, [])
    
    def printStatus(self):
        status = self.status

        # Check in application mode
        FW_MODE = getBit(status, 7)
        print(f'FW_MODE: {FW_MODE}')
        if FW_MODE == 0: 
            print("Sensor is in boot mode")
            print("Starting application...")
            self.startApp()
            sleep(0.3)
            print("Getting new status...")
            self.updateStatus()
            return
        
        # Check app is valid
        APP_VALID = getBit(status, 4)
        print(f'APP_VALID: {APP_VALID}')
        assert APP_VALID == 1, "ERROR: Sensor does not have valid application firmware"

        # Check for data / errors
        DATA_READY = getBit(status, 3)
        print(f'DATA_READY: {DATA_READY}')
        ERROR = getBit(status, 0)
        print(f'ERROR: {ERROR}')
        if DATA_READY == 1: print('Data is ready to be read')
        if ERROR == 1: print('Read ERROR_ID')

    def updateMode(self):
        self.mode = self.bus.read_byte_data(self.ADDR, self.REGS.MODE)
        self.printMode()

    def printMode(self):
        mode = self.mode
        DRIVE_MODE = f"{getBit(mode, 6)}{getBit(mode, 5)}{getBit(mode, 4)}"
        if DRIVE_MODE == "000": 
            print("Mode 0 - Idle (Measurements are disabled in this mode)")
            print("Setting sensor to Mode 1...")
            self.setMode()
            sleep(0.3)
            print("Getting new mode...")
            self.updateMode()
            return
        elif DRIVE_MODE == "001": print("Mode 1 - Constant power mode, IAQ measurement every second")
        elif DRIVE_MODE == "010": print("Mode 2 - Pulse heating mode IAQ measurement every 10 seconds")
        elif DRIVE_MODE == "011": print("Mode 3 - Low power pulse heating mode IAQ measurement every 60 seconds")
        elif DRIVE_MODE == "100": print("Mode 4 - Constant power mode, sensor measurement every 250ms, use RAW_DATA")
        else: assert 0, f"Invalid DRIVE_MODE: {DRIVE_MODE}"

        INT_DATARDY = getBit(mode, 3)
        if INT_DATARDY:
            print("DATA INTERRUPT ENABLED: nINT signal will be driven low when a new sample is ready in ALG_RESULT_DATA, and will stop being driven low when ALG_RESULT_DATA is read on the I2C interface.")
        else:
            print("DATA INTERRUPT DISABLED")
        
        INT_THRESH = getBit(mode, 2)
        print(f"INT_THRESH: {INT_THRESH}")
        assert INT_THRESH == 0, print("THRESHOLD INTERRUPT ENABLED, WE AREN'T USING THRESHOLDS")

    def setMode(self, newMode=1, interrupt=0):
        assert newMode >= 0 and newMode <= 4, print(f"INVALID MODE: {newMode} (Please use a mode in the range [0-4])")
        DRIVE_MODE = "{0:03b}".format(newMode)
        assert interrupt == 0 or interrupt == 1, print(f"INVALID INTERRUPT: {interrupt} (Please use 0 or 1 to disable / enable interrupt)")
        INT_DATARDY = "{0:01b}".format(interrupt)
        data = bitStringToByte(f"0{DRIVE_MODE}{INT_DATARDY}000")
        self.bus.write_byte_data(self.ADDR, self.REGS.MODE, data)


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

def main():
    bus = smbus2.SMBus(1)
    sensor = SENSOR(0x5A, SENSOR_REGISTERS(), bus) # Initialises sensor
    if sensor.new_data:
        sensor.getCO2()


if __name__ == "__main__":
    main()
