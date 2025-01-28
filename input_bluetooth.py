import serial
import time
import math

class InputBluetooth():
    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.altitude = 0
        self.speed = 0
        self.lat = 0
        self.lon = 0

        self.bluetooth = serial.Serial('COM9', 115200, timeout=1000)
    
    def getData(self):
        data = self.bluetooth.readline()
        print(data)

        t = time.time()

        self.roll = 5 * math.cos(t / 1)
        self.pitch = 10 * math.sin(t / 1)
        self.altitude = 50 - 30 * math.sin(t / 1)
        self.speed = 10 - 5 * math.cos(t / 1)
        self.lat = 33.017826
        self.lon = -118.602432
        self.heading = 30*math.sin(t)

    def send(self):
        return