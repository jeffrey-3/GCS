import serial
import time
import math
import struct
from lib.cobs import cobs
from input import Input

class InputBluetooth(Input):
    def __init__(self):
        super().__init__()

        self.bluetooth = serial.Serial('COM9', 115200, timeout=1000)
        self.prev_send_time = time.time()
        self.prev_recv_time = time.time()
    
    def getData(self):
        if self.bluetooth.in_waiting:
            packet_raw = self.bluetooth.read(40)

            packet = packet_raw[1:] # Remove start byte
            packet = cobs.decode(packet) # Decode COBS

            payload_type = packet[0]
            
            # Figure out what type of payload
            if payload_type == 0: # Telemetry payload
                packet = packet[1:-15] # Remove empty bytes at end of packet and the "payload type" byte at start of packet
                packet = struct.unpack("<hhHhHffBBB?", packet) # Use endian to remove padding
                self.flight_data.roll = float(packet[0]) / 100
                self.flight_data.pitch = float(packet[1]) / 100
                self.flight_data.heading = float(packet[2]) / 10
                self.flight_data.altitude = float(packet[3]) / 10
                self.flight_data.speed = float(packet[4]) / 10
                self.flight_data.lat = packet[5]
                self.flight_data.lon = packet[6]
                self.flight_data.mode_id = packet[7]
                self.flight_data.wp_idx = packet[8]
                self.flight_data.sats = packet[9]
                self.flight_data.gps_fix = packet[10]

                self.flight_data.packet_rate = 1 / (time.time() - self.prev_recv_time)
                self.prev_recv_time = time.time()

                return True
            elif payload_type == 1 or payload_type == 2 or payload_type == 3: # Command/waypoint/landing target acknowledgement payload
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
        return bytes([0x00]) + cobs.encode(command_payload)
    
    def generate_waypoint_packet(self, waypoint, waypoint_index):
        # Interface layer
        waypoint_payload = bytearray([0x00] * 38)
        waypoint_payload[0] = 2 # Payload type
        waypoint_payload[1] = waypoint_index # Waypoint index
        waypoint_payload[2:14] = struct.pack("3f", waypoint[0], waypoint[1], waypoint[2])

        # T ransport protocol layer
        return bytes([0x00]) + cobs.encode(waypoint_payload)

    def generate_landing_target_packet(self, lat, lon, hdg):
        landing_target_payload = bytearray([0x00] * 38)
        landing_target_payload[0] = 3
        landing_target_payload[1:13] = struct.pack("3f", lat, lon, hdg)
        return bytes([0x00]) + cobs.encode(landing_target_payload)
    
    def send(self):
        if len(self.command_queue) > 0 and time.time() - self.prev_send_time > 0.1:
            self.bluetooth.write(self.command_queue[0])
            self.prev_send_time = time.time()
    
    def append_queue(self, packet):
        if not packet in self.command_queue:
            self.command_queue.append(packet)