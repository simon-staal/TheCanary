import smbus2
import time

def convertTemp(measurement):
    result = (175.72*measurement)/65536 - 46.85
    return result
    
#create the i2c bus
# >>> import smbus2
bus = smbus2.SMBus(1)
#send the measure temperature command
meas_temp= smbus2.i2c_msg.write(0x40,[0xf3])
bus.i2c_rdwr(meas_temp)

#wait for measurement
time.sleep(0.1)

#send the read temperature command and read two bytes of data
read_result = smbus2.i2c_msg.read(0x40,2)
bus.i2c_rdwr(read_result)

#convert the result to an int
rd_temp = int.from_bytes(read_result.buf[0]+read_result.buf[1],"big")
temp = convertTemp(rd_temp)
print(temp)