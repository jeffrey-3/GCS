import serial
import time
import math
import struct

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
        if self.bluetooth.in_waiting > 0:
            data = self.bluetooth.read_all() # Flush buffer
            idx = data.rfind(b'\n')
            data = data[idx-29:idx+1]
            data = struct.unpack('fffffff?c', data)
            print(data)

            valid = True
            for i in range(len(data) - 1): # Ignore the "\n" footer at the end
                if abs(data[i]) > 1000000000:
                    valid = False

            if valid:
                self.roll = data[0]
                self.pitch = data[1]
                self.heading = data[2]
                self.altitude = data[3]
                self.speed = data[4]
                self.lat = data[5]
                self.lon = data[6]

    def send(self):
        self.bluetooth.write(b'Hello\n')