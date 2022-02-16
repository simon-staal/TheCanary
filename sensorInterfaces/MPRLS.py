import smbus2
from time import sleep
from numpy import byte
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

    def __init__(self, addr, bus):
        self.ADDR = addr
        self.bus = bus
        self.readCmd = bytearray([0x30,0xAA, 0, 0])

    def takeReading(self):

        print(byte(0x31))
        for i in range(4):
            print(self.readCmd[i])
            self.bus.write_byte_data(0x18, 0, self.readCmd[i])

    def readMeasurement(self):
        read = smbus2.i2c_msg.read(0x18, 4)
        self.bus.i2c_rdwr(read)
        return int.from_bytes(read.buf[0]+read.buf[1]+read.buf[2]+read.buf[3], 'big')

    def getPressure(self):
        self.takeReading()
        sleep(0.001)
        tmp = self.readMeasurement()
        print("read data: ", tmp)    

def main():
    bus = smbus2.SMBus(1)
    sensor = MPRLS(0x18, bus) # Initialises sensor
    while(1):
        sleep(1)
        sensor.getPressure()
        sleep(2)



if __name__ == "__main__":
    main()
