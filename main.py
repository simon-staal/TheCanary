from pydoc import cli
import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.Si7021 as Si7021
import sensorInterfaces.bmp280 as bmp280
import smbus2
import time
import paho.mqtt.client as mqtt
import DataProcessing as Data
import numpy as np


#set up sensors - i2c connections + mqtt
def initSensors():
    bus = smbus2.SMBus(1)
    airQualitySensor = ccs811.SENSOR(bus)
    tempHumiditySensor = Si7021.SENSOR(bus)
    airPressureSensor = bmp280.Sensor(bus)

    co2Data = Data(airQualitySensor, airQualitySensor.getco2())
    tempData = Data(tempHumiditySensor, tempHumiditySensor.getTemp(), )
    humidityData = Data(tempHumiditySensor, tempHumiditySensor.getHumid())
    airPressureData = Data(airPressureSensor, airPressureSensor.pressure)

    for item in {co2Data, tempData, humidityData, airPressureData}:
        item.last20val = np.full_like(np.arange(6, dtype=float), item.getReading())

    return airQualitySensor, tempHumiditySensor, airPressureSensor

def initMQTT(): 
    client = mqtt.Client()
    client.tls_set(ca_certs="mosquitto.org.crt",\
                certfile="/MQTT/client.crt",\
                keyfile="/MQTT/client.key")

    returnCode = client.connect("test.mosquitto.org",port=8884)
    print(f"connect status: {mqtt.error_string(returnCode)}\n")
    time.sleep(1)
    print("Subscribing to topic","IC.embedded/TeamEpicGamers/#")
    client.subscribe("IC.embedded/TeamEpicGamers/test")

    # MsgInfo = client.publish("IC.embedded/TeamEpicGamers/test","hello")
    # print("...")
    # print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

    return client


def main():
    
    airQuality, tempHumid, airPresssure = initSensors()
    client = initMQTT()


    
    
if __name__ == "__main__":
    main()