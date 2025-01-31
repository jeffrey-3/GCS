import serial
import time
import math
import struct
from cobs import cobs

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
            data_raw = self.bluetooth.read_all() # Flush buffer
            idx = data_raw.rfind(b'\n')
            if data_raw[idx-32] == 10: # Go back to previous packet and see if it ends with correct footer
                data = struct.unpack('fffffff?c', data_raw[idx-29:idx+1])
                print(data)
                self.roll = data[0]
                self.pitch = data[1]
                self.heading = data[2]
                self.altitude = data[3]
                self.speed = data[4]
                self.lat = data[5]
                self.lon = data[6]

                return True
        return False

    def send(self):
        # Interface layer
        command_payload = bytearray([0x00] * 38)
        command_payload[0] = 0b00000001 # Payload type
        command_payload[1] = 0b00000000 # Command type

        # Transport protocol layer
        packet = bytes([0x00]) + cobs.encode(command_payload)

        self.bluetooth.write(packet)