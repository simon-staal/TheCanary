from codecs import getreader
from time import sleep
import numpy as np
import json

GREEN = 0
AMBER = 1
RED = 2

class Data():

    def __init__(self,Sensor, dataFunc, val20, client):
        self.last20Val = val20
        self.sensor = Sensor
        self.minVal = 1
        self.maxVal = 1
        self.pollingRate = 0.20
        self.defaultPollingRate = 0.20
        self.dangerLevel = GREEN #DFS would actually be useful here. levels could be green amber red
        self.dataFunc = dataFunc
        self.client = client
        self.lastReading

    def getReading(self):
        return self.dataFunc

    @property
    def avgVal(self):
        return np.mean(self.last20Val)

    @property
    def consistentBadValues(self):
        return self.avgVal > self.maxVal | self.avgVal < self.minVal

    @property
    def worryingValue(self):
        return self.lastReading > self.maxVal | self.lastReading < self.minVal
   
    def processData(self):
        self.lastReading = self.getReading
        self.last20Val.pop
        self.last20Val.append(self.lastReading)
        self.checkSafety()
        return

    def checkSafety(self):   
        #this as a whole looks super inefficient refactor later 
        if(self.consistentBadValues):
            self.dangerLevel = RED
            self.pollinRate = 6 # idk if i need this
        elif(self.worryingValue):
            self.dangerLevel = AMBER
            self.pollingRate = 5
        else:
            self.dangerLevel = GREEN
            self.pollingRate = self.defaultPollingRate
        return

    def getData(self):
        self.processData()
        return json.dumps({"Latest Reading":self.lastRead, "Average Value":self.avgVal, "Danger Level":self.dangerLevel})

