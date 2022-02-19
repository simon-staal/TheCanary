from pydoc import cli
import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.Si7021 as Si7021
import sensorInterfaces.bmp280 as bmp280
import smbus2
import time
import paho.mqtt.client as mqtt
import DataProcessing as Data
import numpy as np
import json



#set up sensors - i2c connections + mqtt
def initSensors():
    bus = smbus2.SMBus(1)
    airQualitySensor = ccs811.SENSOR(bus)
    tempHumiditySensor = Si7021.SENSOR(bus)
    airPressureSensor = bmp280.Sensor(bus)

    co2Data = Data.Data(airQualitySensor, airQualitySensor.getco2())
    tempData = Data.Data(tempHumiditySensor, tempHumiditySensor.getTemp())
    humidityData = Data.Data(tempHumiditySensor, tempHumiditySensor.getHumid())
    airPressureData = Data.Data(airPressureSensor, airPressureSensor.pressure)

    for item in {co2Data, tempData, humidityData, airPressureData}:
        item.last20val = np.full_like(np.arange(6, dtype=float), item.getReading())

    return co2Data, tempData, humidityData, airPressureData

def shutDown():
    #might put other stuff here
    print("Ending Program")
    exit()

def onMessage(client, userdata, message):
    msg = json.loads(message.payload.decode("utf-8"))
    if(msg is "end"):## just placeholeder atm
        shutDown()
    print("Received message:{} on topic {}".format(str(message.payload.decode("utf-8")), message.topic))

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

    client.on_message = onMessage

    return client

def sendInfo(msg, client):
    MsgInfo = client.publish("sensor/",msg)
    print("...")
    print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

def main():
    
    co2, temp, humidity, airPresssure = initSensors()
    client = initMQTT()
    
    while(1): # placeholder gonna figure out different sensor pollrates 
        for i in {co2, temp, humidity, airPresssure}:
            sendInfo(i.getData(), client)
        time.sleep(i.pollRate())


    
    
if __name__ == "__main__":
    main()