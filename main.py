import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.MPRLS as MPRLS
import sensorInterfaces.Si7021 as Si7021
import smbus2
import time

def main():
    bus = smbus2.SMBus(1)
    airQualitySensor = ccs811.SENSOR(bus)
    airTempHumidSensor = Si7021.TH_SENSOR(bus)
    
    
if __name__ == "__main__":
    main()