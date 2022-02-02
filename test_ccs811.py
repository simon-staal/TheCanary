import smbus2

SLAVE_ADDR = 0x5A

def getBit(val, idx):
    return (val & (1 << idx)) >> idx

def print_status(status):
    FW_MODE = getBit(status, 7)
    print(f'FW_MODE: {FW_MODE}')
    assert FW_MODE == 1, "ERROR: Sensor is in boot mode"
    APP_VALID = getBit(status, 4)
    print(f'APP_VALID: {APP_VALID}')
    assert APP_VALID == 1, "ERROR: Sensor does not have valid application firmware"
    DATA_READY = getBit(status, 3)
    print(f'DATA_READY: {DATA_READY}')
    ERROR = getBit(status, 0)
    print(f'ERROR: {ERROR}')
    if DATA_READY == 1: print('Data is ready to be read')
    if ERROR == 1: print('Read ERROR_ID')

bus = smbus2.SMBus(1)

status = bus.read_byte_data(SLAVE_ADDR, 0x00)

print_status(status)
