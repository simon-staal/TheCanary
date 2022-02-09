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
        self.out = bytearray(4)

    def readReq(self):
        self.readCmd[0] = 0x18
        self.readCmd[1] = 0xAA
        self.readCmd[2] = 0
        self.readCmd[3] = 0
        self.bus.write_i2c_block_data(self.ADDR, 0, self.readCmd)

        #msg = smbus2.i2c_msg.write(self.ADDR, self.readCmd)
        #self.bus.i2c_rdwr(msg)



    def getPressure(self):
        self.readReq()
        sleep(0.01)       
        print(self.bus.read_i2c_block_data(self.ADDR, 0, 4))

        #print("Current Status : " ,status)
        #print("Pressure Reading : ", pressure)


def main():
    bus = smbus2.SMBus(2)
    sensor = MPRLS(0x18, bus) # Initialises sensor
    while(1):
        sleep(2)
        sensor.getPressure()
        sleep(2)



if __name__ == "__main__":
    main()
