import math
import time
from input import Input

class InputRandom(Input):
    def __init__(self):
        super().__init__()
    
    def getData(self):
        t = time.time()

        self.flight_data.roll = 5 * math.cos(t / 1)
        self.flight_data.pitch = 10 * math.sin(t / 1)
        self.flight_data.altitude = 50 - 30 * math.sin(t / 1)
        self.flight_data.speed = 10 - 5 * math.cos(t / 1)
        self.flight_data.lat = 33.02
        self.flight_data.lon = -118.6
        self.flight_data.heading = abs(360*math.sin(t/2))
        self.flight_data.pitch_setpoint = 30*math.cos(t)
        self.flight_data.heading_setpoint = 10*math.sin(t)

        return True