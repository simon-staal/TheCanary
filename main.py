from pydoc import cli
import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.Si7021 as Si7021
import sensorInterfaces.bmp280 as bmp280
import smbus2
import time
import paho.mqtt.client as mqtt
import DataProcessing as Data
from DataProcessing import Data
import numpy as np
import json

CanaryId = "noId"

#set up sensors - i2c connections + mqtt
def initSensors():
    bus = smbus2.SMBus(1)
    airQualitySensor = ccs811.SENSOR(bus)
    tempHumiditySensor = Si7021.SENSOR(bus)
    airPressureSensor = bmp280.Sensor(bus)
    airPressureSensor.mode = bmp280.NORMAL_MODE

    time.sleep(2)

    co2Data = Data("CO2", airQualitySensor.getco2)
    tempData = Data("Temperature", tempHumiditySensor.getTemp)
    humidityData = Data("Humidity", tempHumiditySensor.getHumid)
    airPressureData = Data("Pressure", airPressureSensor.pressure)
    time.sleep(1)
    tvocData = Data("TVOC", airQualitySensor.getTvoc)

    return co2Data, tempData, humidityData, airPressureData, tvocData

def onMessage(client, userdata, message):
    msg = json.loads(message.payload.decode("utf-8"))
    print("Received message:{} on topic {}".format(str(msg), message.topic))

def onConnect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("test/#")
    client.subscribe("sensor/instructions/#")
    

def initMQTT(): 
    client = mqtt.Client()
    client.on_message = onMessage
    client.on_connect = onConnect
    client.tls_set(ca_certs='AWS/cert/ca.crt', certfile='AWS/cert/pi.crt', keyfile='AWS/cert/pi.key')
    client.username_pw_set('sensor', '2Q7!#fXb6zcaU*DY')

    returnCode = client.connect("thecanary.duckdns.org", 8883, 60)
    print(f"connect status: {mqtt.error_string(returnCode)}\n")
    time.sleep(1)

    return client

def sendInfo(data, client):
    msg = {"id":CanaryId}.update({"data":data})
    MsgInfo = client.publish("sensor/data", json.dumps(msg))
    print("...")
    print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

def main():
    print("start of main")
    co2, temp, humidity, airPresssure, tvoc = initSensors()
    print("mqtt")
    client = initMQTT()
    
    while(1): # placeholder gonna figure out different sensor pollrates
        data = {}
        client.loop()
        for i in {co2, temp, humidity, airPresssure, tvoc}:
            reading = i.oneReading()
            print("measured data", reading)
            data.update(reading)
        sendInfo(data, client)
        time.sleep(co2.pollRate)

    
    
if __name__ == "__main__":
    main()