from codecs import getreader
from time import sleep
import numpy as np
import json
import sensorInterfaces.ccs811 as ccs811
import sensorInterfaces.Si7021 as Si7021
import sensorInterfaces.bmp280 as bmp280

GREEN = 0
AMBER = 1
RED = 2

class Data():

    def __init__(self, sensorName, dataFunc):
        self.last20Val = np.full_like(np.arange(20, dtype=np.double), dataFunc())
        self.sensor = sensorName
        self.minVal = 0
        self.maxVal = 1000000000
        self.pollingRate = 0.20
        self.defaultPollingRate = 0.20
        self.dangerLevel = GREEN
        self.getDataReading = dataFunc
        self.lastReading = 0
        self.avgVal = np.mean(self.last20Val)

    def getReading(self):
        return self.getDataReading()

    def oneReading(self):
        return {self.sensor: self.getReading()}

    def setDefaultPollingRate(self, pollRate):
        self.defaultPollingRate = pollRate

    def findAvgVal(self):
        self.avgVal = np.mean(self.last20Val)

    def setThresholdValues(self,min,max):
        self.minVal = min
        self.maxVal = max

    @property
    def consistentBadValues(self):
        return (self.avgVal > self.maxVal or self.avgVal < self.minVal)

    @property
    def pollRate(self):
        return 1/self.pollingRate

    @property
    def getDangerLevel(self):
        return self.dangerLevel

    @property
    def worryingValue(self):
        return (self.lastReading > self.maxVal or self.lastReading < self.minVal)
   
    def processData(self):
        self.lastReading = self.getReading()
        self.last20Val = np.delete(self.last20Val, 0)
        self.last20Val = np.append(self.last20Val, self.lastReading)
        self.findAvgVal()
        self.checkSafety()
        return {self.sensor: self.lastReading}, self.dangerLevel

    def checkSafety(self):   
        #this as a whole looks super inefficient refactor later 
        if(self.consistentBadValues):
            self.dangerLevel = RED
            self.pollinRate = 1
        elif(self.worryingValue):
            self.dangerLevel = AMBER
            if 0.5 > self.pollingRate:
                self.pollingRate = 0.5
        else:
            self.dangerLevel = GREEN
            self.pollingRate = self.defaultPollingRate
        return

    def getData(self):
        self.processData()
        return {"Sensor":self.sensor, "Latest Reading":self.lastReading, "Average Value":self.avgVal, "Danger Level":self.dangerLevel}

