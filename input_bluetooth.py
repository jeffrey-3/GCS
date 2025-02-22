import serial
import time
import struct
from lib.cobs import cobs
from input import Input
from generate_packet import *

class InputBluetooth(Input):
    def __init__(self):
        super().__init__()

        self.bluetooth = serial.Serial('COM9', 115200, timeout=1000)
        self.prev_send_time = time.time()
        self.prev_recv_time = time.time()
    
    # Move this to main
    def getData(self):
        while self.bluetooth.in_waiting:
            # Find start byte
            start_byte = self.bluetooth.read(1)
            if start_byte == b'\x00':
                # Get length byte
                payload_length = struct.decode("B", self.bluetooth.read(1))
                
                # Get payload
                payload = cobs.decode(self.bluetooth.read(payload_length + 1))
                
                # Figure out what type of payload from message ID byte
                payload_type = payload[0]
                if payload_type == 0: # Telemetry payload
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
                    if payload in self.command_queue:
                        self.command_queue.remove(payload)
        return False
    
    def send(self):
        if len(self.command_queue) > 0 and time.time() - self.prev_send_time > 0.1:
            self.bluetooth.write(get_pkt(self.command_queue[0]))
            self.prev_send_time = time.time()
    
    def append_queue(self, payload):
        if not payload in self.command_queue:
            self.command_queue.append(payload)