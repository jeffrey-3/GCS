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
        self.mode_id = -1

        # When command needs to be sent, it gets added here.
        # When it recieves acknowledgement, it gets removed
        self.command_queue = []

        self.bluetooth = serial.Serial('COM9', 115200, timeout=1000)
    
    def getData(self):
        if self.bluetooth.in_waiting > 0:
            data_raw = self.bluetooth.read_all() # Flush buffer
            last_idx = data_raw.rfind(0b00000000)
            second_last_idx = data_raw.rfind(0b00000000, 0, last_idx)
            packet_raw = data_raw[second_last_idx:last_idx]

            if len(packet_raw) == 40:
                packet = packet_raw[1:] # Remove start byte
                packet = cobs.decode(packet) # Decode COBS
                
                # Figure out what type of payload
                if packet[0] == 0: # Telemetry payload
                    packet = packet[1:-8] # Remove empty bytes and the "payload type" byte
                    packet = struct.unpack("<fffffffB", packet) # Use endian to remove padding
                    print(packet)
                    self.roll = packet[0]
                    self.pitch = packet[1]
                    self.heading = packet[2]
                    self.altitude = packet[3]
                    self.speed = packet[4]
                    self.lat = packet[5]
                    self.lon = packet[6]
                    self.mode_id = packet[7]

                    return True
                elif packet[0] == 1: # Command payload
                    return False
                elif packet[0] == 2: # Waypoint payload
                    if packet_raw in self.command_queue:
                        self.command_queue.remove(packet_raw)
                    return False
        return False

    def generate_command_packet(self, command):
        # Interface layer
        command_payload = bytearray([0x00] * 38)
        command_payload[0] = 1 # Payload type
        command_payload[1] = command # Command

        # Transport protocol layer
        packet = bytes([0x00]) + cobs.encode(command_payload)

        return packet
    
    def generate_waypoint_packet(self, waypoint, waypoint_index):
        # Interface layer
        waypoint_payload = bytearray([0x00] * 38)
        waypoint_payload[0] = 2 # Payload type
        waypoint_payload[1] = waypoint_index # Waypoint index
        waypoint_payload[2:14] = struct.pack("3f", waypoint[0], waypoint[1], waypoint[2])

        # Transport protocol layer
        packet = bytes([0x00]) + cobs.encode(waypoint_payload)

        return packet
    
    def send(self):
        if len(self.command_queue) > 0:
            # print("send")
            self.bluetooth.write(self.command_queue[0])
    
    def append_queue(self, packet):
        self.command_queue.append(packet)