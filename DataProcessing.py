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

    def setDefaultPollingRate(self, pollRate):
        self.defaultPollingRate = pollRate

    def findAvgVal(self):
        self.avgVal = np.mean(self.last20Val)

    @property
    def consistentBadValues(self):
        return (self.avgVal > self.maxVal or self.avgVal < self.minVal)

    @property
    def pollRate(self):
        return 1/self.pollingRate

    @property
    def worryingValue(self):
        return (self.lastReading > self.maxVal or self.lastReading < self.minVal)
   
    def processData(self):
        self.lastReading = self.getReading()
        self.last20Val = self.last20Val[1:]
        np.append(self.last20Val, self.lastReading)
        self.findAvgVal()
        self.checkSafety()
        return

    def checkSafety(self):   
        #this as a whole looks super inefficient refactor later 
        if(self.consistentBadValues):
            self.dangerLevel = RED
            self.pollinRate = self.defaultPollingRate * 8
        elif(self.worryingValue):
            self.dangerLevel = AMBER
            self.pollingRate = self.defaultPollingRate * 4
        else:
            self.dangerLevel = GREEN
            self.pollingRate = self.defaultPollingRate
        return

    def getData(self):
        self.processData()
        return json.dumps({"Sensor":self.sensor, "Latest Reading":self.lastReading, "Average Value":self.avgVal, "Danger Level":self.dangerLevel})

