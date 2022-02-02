import smbus2
from time import sleep

SLAVE_ADDR = 0x5A # Can be 0x5A

# Slave registers to read and write
DEVICE_REG_STATUS = 0x00
DEVICE_REG_MEAS_MODE = 0x01
DEVICE_REG_ALG_RESULT_DATA = 0x02
DEVICE_REG_ERROR_ID = 0xE0
DEVICE_REG_APP_START = 0xF4

# Slave register read values
DEVICE_STATE_BOOT = 0x10
DEVICE_STATE_APP = 0x90
DEVICE_STATE_APP_WITH_DATA = 0x98

# Slave register write values
DEVICE_SET_MODE_10S = [0x10]
DEVICE_SET_SW_RESET = [0x11, 0xE5, 0x72, 0x8A]

# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
i2c_bus = smbus2.SMBus(1)

def read_i2c_bus_dev(dev_reg, read_len):
    return i2c_bus.read_i2c_block_data(SLAVE_ADDR, dev_reg, read_len)

def write_i2c_bus_dev(dev_reg, write_data):
    i2c_bus.write_i2c_block_data(SLAVE_ADDR, dev_reg, write_data)

try:
    print("Hello from python")
    if read_i2c_bus_dev(DEVICE_REG_STATUS, 1)[0] == DEVICE_STATE_BOOT:
        write_i2c_bus_dev(DEVICE_REG_APP_START, []) # empty write
        write_i2c_bus_dev(DEVICE_REG_MEAS_MODE, DEVICE_SET_MODE_10S)

    read_i2c_bus_dev(DEVICE_REG_ERROR_ID, 1) # clear any errors

    timeout_in_seconds = 30

    while (timeout_in_seconds and
           (read_i2c_bus_dev(DEVICE_REG_STATUS, 1)[0] !=
            DEVICE_STATE_APP_WITH_DATA)):
              sleep(5)
              timeout_in_seconds -= 5

    if not timeout_in_seconds:
        raise

    read_data = read_i2c_bus_dev(DEVICE_REG_ALG_RESULT_DATA, 8)

    eCO2_reading = (read_data[0] << 8) | read_data[1]
    eTVOC_reading = (read_data[2] << 8) | read_data[3]

    # Return some Dialtone!
    print ('{{"chans":['
              '{{"ch_idx":0,"ch_data":[{{"data_idx":0,"units":1,"val":{0}}}]}},'
              '{{"ch_idx":1,"ch_data":[{{"data_idx":0,"units":1,"val":{1}}}]}}'
           ']}}').format(eCO2_reading, eTVOC_reading)

except Exception as e:
    pass
finally:
    i2c_bus.close()
