import math
import time
import random
from input import Input

class InputRandom(Input):
    def __init__(self):
        super().__init__()
    
    def getData(self):
        t = time.time()

        self.flight_data.roll = 5 * math.cos(t)
        self.flight_data.pitch = 10 * math.sin(t)
        self.flight_data.altitude = 50 - 30 * math.sin(t)
        self.flight_data.speed = 10 - 5 * math.cos(t)
        self.flight_data.lat = 33.02 + 0.005 * math.sin(t/6)
        self.flight_data.lon = -118.6 + 0.005 * math.cos(t/6)
        self.flight_data.heading = 180 + 180*math.sin(t/5)
        self.flight_data.pitch_setpoint = 30*math.cos(t)
        self.flight_data.heading_setpoint = 10*math.sin(t)

        self.flight_data.mode_id = 2
        self.flight_data.cell_voltage = random.uniform(3.5, 3.8)
        self.flight_data.sats = random.randint(10, 11)
        self.flight_data.gps_fix = True
        self.flight_data.packet_rate = random.uniform(18, 20)
        self.flight_data.current = random.uniform(8, 10)

        return True