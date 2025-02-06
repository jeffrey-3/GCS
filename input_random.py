import math
import time
from input import Input

class InputRandom(Input):
    def __init__(self):
        super().__init__()
    
    def getData(self):
        t = time.time()
        self.roll = 5 * math.cos(t / 1)
        self.pitch = 10 * math.sin(t / 1)
        self.altitude = 50 - 30 * math.sin(t / 1)
        self.speed = 10 - 5 * math.cos(t / 1)
        self.lat = 33.02
        self.lon = -118.6
        self.heading = abs(360*math.sin(t/2))
        self.pitch_setpoint = 30*math.cos(t)
        self.heading_setpoint = 30*math.sin(t)

        return True