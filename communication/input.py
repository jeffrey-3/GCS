from app.utils.data_structures import *
import time
import threading
import serial
import struct
import random
from lib.cobs import cobs
import math
from communication.generate_packet import *
from PyQt5.QtCore import *

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

class Input(QObject):
    flight_data_updated = pyqtSignal(FlightData)

    def __init__(self):
        super().__init__()
        self.flight_data = FlightData()
        self.command_queue = PayloadQueue()
        self.command_queue.run_cleanup()
        self.ser = None
        self.port = None
        self.prev_send_time = time.time()
        self.prev_recv_time = time.time()
        self.prev_rate_calc_time = time.time()
        self.bytes_read = 0
        self.rate_calc_dt = 1
        self.transmit_dt = 0.5
    
    def connect_and_start_thread(self, port):
        self.port = port
        if not port == 'Testing':
            try:
                self.ser = serial.Serial(port, 115200, timeout=1000)
            except:
                return False
            
        threading.Thread(target=self.recv_thread, daemon=True).start()
        threading.Thread(target=self.transmit_thread, daemon=True).start()
        
        return True
    
    def append_queue(self, payload):
        print("Input append queue")
        self.command_queue.add_payload(payload)
    
    def recv_thread(self):
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
                    data = struct.unpack("<BhhHhHffBBB?h", payload) # Use endian to remove padding
                    self.flight_data.roll = float(data[1]) / 100
                    self.flight_data.pitch = float(data[2]) / 100
                    self.flight_data.heading = float(data[3]) / 10
                    self.flight_data.altitude = float(data[4]) / 10
                    self.flight_data.speed = float(data[5]) / 10
                    self.flight_data.lat = data[6]
                    self.flight_data.lon = data[7]
                    self.flight_data.mode_id = data[8]
                    self.flight_data.wp_idx = data[9]
                    self.flight_data.sats = data[10]
                    self.flight_data.gps_fix = data[11]
                    self.flight_data.alt_setpoint = float(data[12]) / 10

                    self.bytes_read += payload_length + 3 # Add 3 because header
                    if time.time() - self.prev_rate_calc_time >= self.rate_calc_dt:
                        self.flight_data.packet_rate = self.bytes_read / self.rate_calc_dt
                        self.bytes_read = 0
                        self.prev_rate_calc_time = time.time()
                    
                    self.flight_data_updated.emit(self.flight_data)
                elif payload_type == 1 or payload_type == 2 or payload_type == 3 or payload_type == 4: # Command/waypoint/landing target acknowledgement payload
                    self.command_queue.remove_payload(payload)
            except:
                print("Payload unpacking exception occurred")
    
    def execute_testing(self):
        while True:
            t = time.time()
            self.flight_data.roll = 10 * math.cos(t)
            self.flight_data.pitch = 10 * math.sin(t)
            self.flight_data.altitude = 20 - 5 * math.sin(t)
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
            self.flight_data.wp_idx = 2

            self.flight_data_updated.emit(self.flight_data)

            time.sleep(0.03)
    
    def transmit_thread(self):
        while True:
            if not self.port == "Testing":
                if len(self.command_queue.queue) > 0 and time.time() - self.prev_send_time > self.transmit_dt:
                    self.ser.write(get_pkt(self.command_queue.get_payload()))
                    self.prev_send_time = time.time()
                
            self.flight_data.queue_len = len(self.command_queue.queue)

            time.sleep(0.01)