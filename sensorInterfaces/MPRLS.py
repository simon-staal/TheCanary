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

    def __init__(self, addr, bus):
        self.ADDR = addr
        self.bus = bus
        self.readCmd = bytearray(4)

    def readReq(self):
        self.readCmd[0] = 0xAA
        self.readCmd[1] = 0
        self.readCmd[2] = 0
        
        msg = smbus2.i2c_msg.write(self.ADDR, self.readCmd)
        self.bus.i2c_rdwr(msg)



    def getPressure(self):
        self.readReq()
        sleep(0.005)
        msg = smbus2.i2c_msg.read(self.ADDR, 4)
        read = self.bus.i2c_rdwr(msg)
        print(read)
        #print("Current Status : " ,status)
        #print("Pressure Reading : ", pressure)


def main():
    bus = smbus2.SMBus(2)
    sensor = MPRLS(0x18, bus) # Initialises sensor
    while(1):
        sensor.getPressure()
        sleep(4)



if __name__ == "__main__":
    main()
