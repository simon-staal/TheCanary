import smbus2
from time import sleep
from time import time

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

    RESET = 0xFF

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
        self.data = []
        self.initStatus()
        self.printMode()

    def getStatus(self):
        self.status = self.bus.read_byte_data(self.ADDR, self.REGS.STATUS)
        self.printStatus()
        return self.status

    def startApp(self):
        self.bus.write_i2c_block_data(self.ADDR, self.REGS.APP_START, [])
    
    def initStatus(self):
        print("Sensor Initialisation")
        status = self.status
        FW_MODE = getBit(status, 7)
        if FW_MODE != 0:
            print("resetting sensor")
            self.bus.write_i2c_block_data(self.ADDR, self.REGS.RESET, [0x11, 0xE5, 0x72, 0x8A])          
            sleep(0.15)
        self.getStatus()

    def printStatus(self):
        print("==== SENSOR STATUS ====")
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
            self.getStatus()
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
        print("=========================")

    def getMode(self):
        self.mode = self.bus.read_byte_data(self.ADDR, self.REGS.MODE)
        self.printMode()
        return self.mode

    def printMode(self):
        print("==== SENSOR MODE ====")
        mode = self.mode
        DRIVE_MODE = f"{getBit(mode, 6)}{getBit(mode, 5)}{getBit(mode, 4)}"
        if DRIVE_MODE == "000": 
            print("Mode 0 - Idle (Measurements are disabled in this mode)")
            print("Setting sensor to Mode 1...")
            self.setMode()
            sleep(0.3)
            print("Getting new mode...")
            self.getMode()
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

        print("=======================")


    def setMode(self, newMode=1, interrupt=0):
        assert newMode >= 0 and newMode <= 4, print(f"INVALID MODE: {newMode} (Please use a mode in the range [0-4])")
        if newMode != 0 and newMode != 4 and newMode > self.mode:
            print("WARNING: When going to a lower sampling rate, sensor should be set to idle for at least 10 minutes")
            print("WARNING: Setting new mode to 0")
            newMode = 1
        DRIVE_MODE = "{0:03b}".format(newMode)
        assert interrupt == 0 or interrupt == 1, print(f"ERROR: INVALID INTERRUPT: {interrupt} (Please use 0 or 1 to disable / enable interrupt)")
        INT_DATARDY = "{0:01b}".format(interrupt)
        data = bitStringToByte(f"0{DRIVE_MODE}{INT_DATARDY}000")
        self.bus.write_byte_data(self.ADDR, self.REGS.MODE, data)


    def newData(self):
        return getBit(self.status, 3)

    def getData(self):
        data = self.bus.read_i2c_block_data(self.ADDR, self.REGS.ALG_RESULT_DATA, 8)
        co2 = data[0:2]
        tvoc = data[2:4]
        self.status = data[4]
        return {"co2": int.from_bytes(bytes(co2), 'big', signed=False),
                "tvoc": int.from_bytes(bytes(tvoc), 'big', signed=False),
                "status": data[4],
                "error": data[5],
                "rawData": data[6:]}
    
    def getco2(self):
        self.data = self.bus.read_i2c_block_data(self.ADDR, self.REGS.ALG_RESULT_DATA, 8)
        co2 = self.data[0:2]
        return int.from_bytes(bytes(co2), 'big', signed=False)

    def getTvoc(self):
        self.data = self.bus.read_i2c_block_data(self.ADDR, self.REGS.ALG_RESULT_DATA, 8)
        tvoc = self.data[2:4]
        return int.from_bytes(bytes(tvoc), 'big', signed=False)

    def setEnv(self, env):
        # Packet we will send
        newEnv = [0, 0, 0, 0]

        # Convert humidity as per data-sheet
        humidity = env["humidity"]
        humidity = int(humidity * (2 << 8)) # Need to multiply because humidity is a float (cringe -- insert fastsqrt hack here)
        newEnv[1] = humidity & 0xFF
        newEnv[0] = (humidity >> 8) & 0xFF

        # Convert temperature as per data-sheet
        temp = env["temp"] - 25
        temp = int(temp * (2 << 8))
        newEnv[3] = temp & 0xFF
        newEnv[2] = (temp >> 8) & 0xFF

        self.bus.write_i2c_block_data(self.ADDR, self.REGS.ENV_DATA, newEnv)




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
    lastMeasurement = time()
    bus = smbus2.SMBus(1)
    sensor = SENSOR(bus) # Initialises sensor
    while(1):
        if sensor.newData():
            if time() - lastMeasurement > 1:
                res = sensor.getData()
                lastMeasurement = time()
                print(f'CO2 = {res["co2"]}ppm, TVOC = {res["tvoc"]}ppb')
        else:
            sensor.getStatus()


if __name__ == "__main__":
    main()

