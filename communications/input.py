from lib.data_structures.data_structures import *
import time
import threading
import serial
import struct
import random
from lib.cobs import cobs
import math
from communications.generate_packet import *

class PayloadQueue:
    def __init__(self, timeout=5):
        self.queue = []  # List of (payload, expiry_time)
        self.timeout = timeout
        self.lock = threading.Lock()
    
    def add_payload(self, payload):
        """Adds a payload to the queue with a timeout if it doesn't already exist."""
        with self.lock:
            if any(p == payload for p, _ in self.queue):
                return
            expiry_time = time.time() + self.timeout
            self.queue.append((payload, expiry_time))
    
    def remove_payload(self, payload):
        """Removes a payload if it exists in the queue."""
        with self.lock:
            self.queue = [(p, t) for p, t in self.queue if p != payload]
    
    def get_payload(self):
        """Retrieves the next payload to send through radio, if available."""
        with self.lock:
            if self.queue:
                return self.queue[0][0]  # Return the first payload in the queue
        return None
    
    def cleanup(self):
        """Removes expired payloads from the queue."""
        current_time = time.time()
        with self.lock:
            self.queue = [(p, t) for p, t in self.queue if t > current_time]
    
    def run_cleanup(self, interval=1):
        """Runs cleanup periodically in a background thread."""
        def _loop():
            while True:
                time.sleep(interval)
                self.cleanup()
        
        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()

class Input():
    def __init__(self):
        self.flight_data = FlightData()
        self.command_queue = PayloadQueue()
        self.command_queue.run_cleanup()
        self.ser = None
        self.port = None
        self.prev_send_time = time.time()
        self.prev_recv_time = time.time()
    
    def connect(self, port):
        self.port = port
        if not port == 'Testing':
            self.ser = serial.Serial(port, 115200, timeout=1000)
        threading.Thread(target=self.serial_thread, daemon=True).start()
        
    def update(self):
        return self.flight_data
    
    def append_queue(self, payload):
        self.command_queue.add_payload(payload)
    
    def serial_thread(self):
        while True:
            if self.port == "Testing":
                self.execute_testing()
            else:
                self.execute()
    
    def execute(self):
        # Find start byte
        start_byte = self.ser.read(1)
        if start_byte == b'\x00':
            # Get length byte
            payload_length = struct.unpack("B", self.ser.read(1))[0]
            
            # Get payload
            try:
                payload = cobs.decode(self.ser.read(payload_length + 1))
                
                # Figure out what type of payload from message ID byte
                payload_type = payload[0] # Incorrect, need to unpack?
                # print(f"Payload type: {payload_type}")
                if payload_type == 0: # Telemetry payload
                    data = struct.unpack("<BhhHhHffBBB?", payload) # Use endian to remove padding
                    self.flight_data.roll = float(data[1]) / 100
                    self.flight_data.pitch = float(data[2]) / 100
                    self.flight_data.heading = float(data[3]) / 10
                    self.flight_data.altitude = float(data[4]) / 10
                    self.flight_data.speed = float(data[5]) / 10
                    self.flight_data.lat = data[6]
                    self.flight_data.lon = data[7]
                    self.flight_data.mode_id = data[8]
                    self.flight_data.wp_idx = data[0]
                    self.flight_data.sats = data[10]
                    self.flight_data.gps_fix = data[11]
                    self.flight_data.packet_rate = 1 / (time.time() - self.prev_recv_time)
                elif payload_type == 1 or payload_type == 2 or payload_type == 3 or payload_type == 4: # Command/waypoint/landing target acknowledgement payload
                    self.command_queue.remove_payload(payload)
            except:
                print("Payload unpacking exception occurred")
    
    def execute_testing(self):
        while True:
            t = time.time()
            self.flight_data.roll = 10 * math.cos(t)
            self.flight_data.pitch = 10 * math.sin(t)
            self.flight_data.altitude = 50 - 30 * math.sin(t)
            self.flight_data.speed = 10 - 5 * math.cos(t)
            self.flight_data.lat = 43.878258 + 0.0005 * math.sin(t/6)
            self.flight_data.lon = -79.413123 + 0.0005 * math.cos(t/6)
            self.flight_data.heading = 180 + 180*math.sin(t/5)
            self.flight_data.pitch_setpoint = 30*math.cos(t)
            self.flight_data.heading_setpoint = 10*math.sin(t)
            self.flight_data.mode_id = 2
            self.flight_data.cell_voltage = random.uniform(3.5, 3.8)
            self.flight_data.sats = random.randint(10, 11)
            self.flight_data.gps_fix = True
            self.flight_data.packet_rate = random.uniform(18, 20)
            self.flight_data.current = random.uniform(8, 10)

            time.sleep(0.01)
    
    def update(self):
        if not self.port == "Testing":
            if len(self.command_queue.queue) > 0 and time.time() - self.prev_send_time > 0.5:
                self.ser.write(get_pkt(self.command_queue.get_payload()))
                self.prev_send_time = time.time()
            
        self.flight_data.queue_len = len(self.command_queue.queue)

        return self.flight_data