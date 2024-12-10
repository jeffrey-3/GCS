import math
import serial

class Input():
    def __init__(self, mode):
        self.mode = mode
        self.x = 0

        if mode == "bluetooth":
            return
        elif mode == "serial":
            self.init_serial()
        elif mode == "socket":
            return
        elif mode == "random":
            return
        else:
            mode = "random"
    def init_serial(self):
        self.ser = serial.Serial("COM25", 115200)
        while True:
            print(self.ser.readline())
    def getData(self):
        roll = 5 * math.cos(self.x / 20)
        pitch = 10 * math.sin(self.x / 20)
        altitude = 50 - 30 * math.sin(self.x / 20)
        speed = 10 - 5 * math.cos(self.x / 20)

        self.x = self.x + 1

        return (pitch, roll, altitude, speed)