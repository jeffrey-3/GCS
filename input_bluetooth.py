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
            last_idx = data_raw.rfind(0b00000000)
            second_last_idx = data_raw.rfind(0b00000000, 0, last_idx)
            data = data_raw[second_last_idx:last_idx]

            if len(data) == 40:
                data = data[1:] # Remove start byte
                data = cobs.decode(data) # Decode COBS
                
                # Figure out what type of payload
                if data[0] == 0: # Telemetry payload
                    data = data[1:-9] # Remove empty bytes and the "payload type" byte
                    data = struct.unpack("<fffffff", data) # Use endian to remove padding
                    self.roll = data[0]
                    self.pitch = data[1]
                    self.heading = data[2]
                    self.altitude = data[3]
                    self.speed = data[4]
                    self.lat = data[5]
                    self.lon = data[6]
                    print("received telemetry")
                    return True
                elif data[0] == 1: # Command payload
                    print("received command")
                    return False
                elif data[0] == 2: # Waypoint payload
                    print("received waypoint")
                    return False
        return False

    def send(self):
        # Interface layer
        command_payload = bytearray([0x00] * 38)
        command_payload[0] = 0b00000001 # Payload type
        command_payload[1] = 0b00000000 # Command

        # Transport protocol layer
        packet = bytes([0x00]) + cobs.encode(command_payload)

        self.bluetooth.write(packet)
    
    def send_waypoints(self, waypoint, waypoint_index):
        # Interface layer
        waypoint_payload = bytearray([0x00] * 38)
        waypoint_payload[0] = 2 # Payload type
        waypoint_payload[1] = waypoint_index # Waypoint index
        waypoint_payload[2:14] = struct.pack("3f", waypoint[0], waypoint[1], waypoint[2])

        # Transport protocol layer
        packet = bytes([0x00]) + cobs.encode(waypoint_payload)

        self.bluetooth.write(packet)