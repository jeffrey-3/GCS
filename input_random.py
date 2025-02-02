import math
import time

class InputRandom():
    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.altitude = 0
        self.speed = 0
        self.lat = 0
        self.lon = 0
    
    def getData(self):
        t = time.time()

        self.roll = 5 * math.cos(t / 1)
        self.pitch = 10 * math.sin(t / 1)
        self.altitude = 50 - 30 * math.sin(t / 1)
        self.speed = 10 - 5 * math.cos(t / 1)
        self.lat = 33.017826
        self.lon = -118.602432
        self.heading = 30*math.sin(t)

        return True

    def send(self):
        return

    def append_queue(self, packet):
        return
    
    def generate_waypoint_packet(self, waypoint, waypoint_index):
        return