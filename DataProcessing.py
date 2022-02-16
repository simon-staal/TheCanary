from time import sleep
import numpy as np


class Data():


    def __init__(self,Sensor, dataFunc, val20):

        self.last20Val = val20
        self.sensor = Sensor
        self.minVal
        self.maxVal
        self.pollingRate = 0.20
        self.timeInDangerZone = 0
        self.dangerLevel = self.timeInDangerZone/3
        self.getData = dataFunc

    def getReading(self):
        return self.dataFunc     

    def getAvgVal(self):
        return np.mean(self.last20Val)

    def processData(self):
        


    def checkSafety(self):

        
        

    def mainLoop(self):

        self.getData()
        sleep(1/self.pollingRate)
