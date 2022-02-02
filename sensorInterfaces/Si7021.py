import smbus2
from time import sleep

# Helper function to isolate a bit of a given byte
def getBit(val, idx):
    return (val & (1 << idx)) >> idx

# Slave register addresses
class TH_COMMANDS():
    #Takes measurement on temperature
    MEASTEMP = 0xF3 
    #Takes measurement on humidity
    MEASHUMID = 0xF5
    #Reads temperature measurement from last humid read
    RDTEMP = 0xE0
    

# Temperature and Humidity Sensor
class TH_SENSOR():
    # Sensor parameters, change depending on your sensor
    ADDR = 0x40 
    CMND = TH_COMMANDS()

    def __init__(self, bus):
        self.ADDR = 0x40 
        self.REGS = TH_COMMANDS()
        self.bus = bus

    def getTemp(self):
        def convertTemp(measurement):
            result = (175.72*measurement)/65536 - 46.85
            return result
        #send the measure temperature command
        meas_temp = smbus2.i2c_msg.write(0x40,[0xf3])
        self.bus.i2c_rdwr(meas_temp)

        #wait for measurement
        sleep(0.1)

        #send the read temperature command and read two bytes of data
        read_result = smbus2.i2c_msg.read(0x40,2)
        self.bus.i2c_rdwr(read_result)

        #convert the result to an int
        rd_temp = int.from_bytes(read_result.buf[0]+read_result.buf[1],"big")
        return convertTemp(rd_temp)

    def getHumid(self):
        def convertHumid(measurement):
            result = (125*measurement/65536) -6
            return result

        #send the measure Humidity command
        measHumid = smbus2.i2c_msg.write(0x40,[0xf5])
        self.bus.i2c_rdwr(measHumid)

        #wait for measurement
        sleep(0.1)

        #send the read temperature command and read two bytes of data
        read_result = smbus2.i2c_msg.read(0x40,2)
        self.bus.i2c_rdwr(read_result)

        #convert the result to an int
        rdHumid = int.from_bytes(read_result.buf[0]+read_result.buf[1],"big")
        Humidity = convertHumid(rdHumid)
        return Humidity


""" Deal with these commands later
Measure Relative Humidity, Hold Master Mode         0xE5
Measure Relative Humidity, No Hold Master Mode      0xF5
Measure Temperature, Hold Master Mode               0xE3
Measure Temperature, No Hold Master Mode            0xF3
Read Temperature Value from Previous RH Measurement 0xE0
Reset                                               0xFE
Write RH/T User Register 1                          0xE6
Read RH/T User Register 1                           0xE7
Write Heater Control Register                       0x51
Read Heater Control Register                        0x11
Read Electronic ID 1st Byte                         0xFA 0x0F
Read Electronic ID 2nd Byte                         0xFC 0xC9
Read Firmware Revision 0x84                         0xB8
"""

def main():
    bus = smbus2.SMBus(1)
    sensor = TH_SENSOR(bus) # Initialises sensor
    
    print(sensor.getTemp)
    print(sensor.getHumid)


if __name__ == "__main__":
    main()
