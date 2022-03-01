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
import RPi.GPIO as GPIO

GREEN = 17
AMBER = 27
RED = 22

global timePeriod
timePeriod = 5
global CanaryId
CanaryId = 0
global dangerLevel
dangerLevel = 0

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GREEN,GPIO.OUT)
    GPIO.setup(AMBER,GPIO.OUT)
    GPIO.setup(RED,GPIO.OUT)
    GPIO.output(GREEN,GPIO.HIGH)

#set up sensors - i2c connections + mqtt
def initSensors():
    bus = smbus2.SMBus(1)
    time.sleep(1)
    airQualitySensor = ccs811.SENSOR(bus)
    tempHumiditySensor = Si7021.SENSOR(bus)
    airPressureSensor = bmp280.Sensor(bus)

    time.sleep(1)

    co2Data = Data("CO2", airQualitySensor.getco2)
    tempData = Data("Temperature", tempHumiditySensor.getTemp)
    humidityData = Data("Humidity", tempHumiditySensor.getHumid)
    airPressureData = Data("Pressure", airPressureSensor.pressure)
    tvocData = Data("TVOC", airQualitySensor.getTvoc)

    tempData.setThresholdValues(0,23.5)

    return co2Data, tempData, humidityData, airPressureData, tvocData

def onMessage(client, userdata, message):
    global timePeriod
    print("Received message: {} on topic {}".format(str(message.payload.decode("utf-8")), message.topic))
    if message.topic == "sensor/instructions/sampling":
        timePeriod = int(message.payload.decode("utf-8"))

def onConnect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("test/#")
    client.subscribe("sensor/instructions/#")
    client.subscribe("sensor/instructions/sampling")

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
    global dangerLevel
    msg = {"id":CanaryId+1}
    info = {"data": data}
    msg.update(info)
    msg.update({"danger":dangerLevel})
    print("sending to server: ", msg)
    MsgInfo = client.publish("sensor/data", json.dumps(msg))
    print("...")
    print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

def setLEDs(dangerLevels):
    setLED = GREEN
    global dangerLevel
    dangerLevel = 0
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(AMBER,GPIO.LOW)
    GPIO.output(RED,GPIO.LOW)
    for i in dangerLevels:
        if i == 2:
            setLED = RED
            dangerLevel = 2
            break
        elif i == 1:
            setLED = AMBER
            dangerLevel = 1
    
    GPIO.output(setLED,GPIO.HIGH)


def main():
    print("start of main")
    initGPIO()
    co2, temp, humidity, airPresssure, tvoc = initSensors()
    print("mqtt")
    client = initMQTT()
    
    while(1): # placeholder gonna figure out different sensor pollrates
        global CanaryId
        data = {}
        dangerLevels = []
        client.loop()
        for i in {co2, temp, humidity, airPresssure, tvoc}:
            reading, danger = i.processData()
            dangerLevels.append(danger)
            data.update(reading)
        print("data: ", data)
        if(data.get("TVOC") > 2000):
            exit()
        sendInfo(data, client)
        setLEDs(dangerLevels)
        time.sleep(timePeriod)
        CanaryId = (CanaryId + 1) % 4

if __name__ == "__main__":
    main()
