from pydoc import cli
import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.Si7021 as Si7021
import sensorInterfaces.bmp280 as bmp280
import smbus2
import time
import paho.mqtt.client as mqtt
from DataProcessing import Data
import numpy as np
import json

CanaryId = "Canary1"

#set up sensors - i2c connections + mqtt
def initSensors():
    bus = smbus2.SMBus(1)
    #airQualitySensor = ccs811.SENSOR(bus)
    tempHumiditySensor = Si7021.SENSOR(bus)
    #airPressureSensor = bmp280.Sensor(bus)

    #co2Data = Data(airQualitySensor, airQualitySensor.getco2())
    tempData = Data("Temperature Sensor", tempHumiditySensor.getTemp)
    humidityData = Data("Humidity Sensor", tempHumiditySensor.getHumid)
    #airPressureData = Data(airPressureSensor, airPressureSensor.pressure)

    #for item in {co2Data, tempData, humidityData, airPressureData}:
    #    item.last20val = np.full_like(np.arange(6, dtype=float), item.getReading())

    #return co2Data, tempData, humidityData, airPressureData

    #tempData.last20val = np.full_like(np.arange(6, dtype=float), tempData.getReading())
    #humidityData.last20val = np.full_like(np.arange(6, dtype=float), humidityData.getReading())    

    return tempData, humidityData


def shutDown():
    #might put other stuff here
    print("Ending Program")
    exit()

def onMessage(client, userdata, message):
    msg = json.loads(message.payload.decode("utf-8"))
    # if(msg is "end"):## just placeholeder atm
    #     shutDown()
    print("Received message:{} on topic {}".format(str(message.payload.decode("utf-8")), message.topic))

def onConnect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("getId/w/e")
    if CanaryId == "noId":
        client.publish("send connection msg", "hi i connected and have no id give me id")
    else:
        client.publish("send my id","hi my id is " + CanaryId)
    

def initMQTT(): 
    client = mqtt.Client()
    client.on_message = onMessage
    client.on_connect = onConnect
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

def sendInfo(msg, client):
    MsgInfo = client.publish("sensor/",msg)
    print("...")
    print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

def main():
    print("here in main")
    #co2, temp, humidity, airPresssure = initSensors()
    temp, humidity = initSensors()
    print("data initialised")
    #client = initMQTT()
    
    while(1): # placeholder gonna figure out different sensor pollrates 
        #client.loop()
        print("in loop")
        for i in {temp, humidity}:
            print(i.getData())
            print("data now sleep")
            time.sleep(i.pollRate)


    
    
if __name__ == "__main__":
    main()
