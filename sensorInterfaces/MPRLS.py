import smbus2
from time import sleep

# only 1 register 32 bit wide
#
# Write
# SensorAddr : Command : CmdData : CmdData .   All 1 byte
# 
# Read
# Status : SensorData : SensorData : SensorData . Sensor 3 pressure reading data + sensor status byte
#

# Sensor class
class MPRLS():
    # Sensor parameters, change depending on your sensor
    ADDR = 0x18 # 18 for MPRLS

    def __init__(self, addr, bus):
        self.ADDR = addr
        self.bus = bus

    def getPressure(self):
        self.bus.write_i2c_block_data(self.ADDR, 0, 0x18AA0000)
        sleep(0.0005)
        status = self.bus.read_i2c_block_data(self.ADDR, 3, 1)
        pressure = self.bus.read_i2c_block_data(self.ADDR, 0, 3)
        print("Current Status : " ,status)
        print("Pressure Reading : ", pressure)


def main():
    bus = smbus2.SMBus(2)
    sensor = MPRLS(0x18, bus) # Initialises sensor
    while(1):
        sensor.getPressure()
        sleep(4)



if __name__ == "__main__":
    main()
