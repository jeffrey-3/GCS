import time
import threading
import serial
import struct
import random
from lib.cobs import cobs
import math
from communication.generate_packet import *
from PyQt5.QtCore import *
from communication.payload_queue import PayloadQueue
from communication.binary_struct import BinaryStruct

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate
    TRANSMIT_DT = 0.5 # Delta time to transmit packets

    tlm_recv = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._tlm_packet = BinaryStruct("communication/telemetry_format.json") # Latest telemetry packet
        self._queue = PayloadQueue() # Transmit queue
        self._queue_len = 0
        self._rx_byte_rate = 0

        # Serial
        self.ser = None
        self.port = None
    
        self.bytes_read = 0 # Bytes read since last byte rate calculation

        # Time keepers
        self.prev_send_time = time.time() # Time of last transmit
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
    
    def start(self, port):
        self.port = port

        if port != 'Testing':
            try:
                self.ser = serial.Serial(port, 115200, timeout=1000)
            except:
                return False
            
        threading.Thread(target=self.thread, daemon=True).start()
        
        return True
    
    def thread(self):
        while True:
            if self.port == "Testing":
                self.execute_testing()
            else:
                self.execute()
    
    def execute(self):
        # Find start byte
        start_byte = self.ser.read(1)

        # Detect start byte
        if start_byte == b'\x00':
            # Get length byte
            payload_length = self.ser.read(1)[0]
    
            # Get payload and COBS byte
            # Then decode to remove COBS byte and get payload
            payload = cobs.decode(self.ser.read(payload_length + 1))
            
            # Get message ID
            payload_type = payload[0]

            # Figure out what type of payload from message ID
            if payload_type == TELEM_MSG_ID: 
                # Telemetry payload
                self.parse_telemetry(payload, payload_length)
            else:
                # If acknowledgement received, remove from queue
                self._queue.remove_payload(payload)
        
        elapsed_time = time.time() - self.prev_send_time
        if len(self._queue.queue) > 0 and elapsed_time > self.TRANSMIT_DT:
            self.ser.write(get_pkt(self._queue.get_payload()))
            self.prev_send_time = time.time()
                
        self.flight_data.queue_len = len(self._queue.queue)
    
    def execute_testing(self):
        while True:
            t = time.time()
            self._tlm_packet.set_data(
                roll = 10 * math.cos(t),
                pitch = 10 * math.sin(t),
                heading = 180 + 180*math.sin(t/5),
                altitude = 20 - 5 * math.sin(t),
                airspeed = 10 - 5 * math.cos(t),
                altitude_setpoint = 0,
                gnss_latitude = 43.878258 + 0.0005 * math.sin(t/6),
                gnss_longitude = -79.413123 + 0.0005 * math.cos(t/6),
                position_estimate_north = 0,
                position_estimate_east = 0,
                mode_id = 2,
                target_waypoint_index = 2,
                cell_voltage = random.uniform(3.5, 3.8),
                battery_current = random.uniform(8, 10),
                capacity_consumed = 0,
                autopilot_current = 0,
                gps_sats = random.randint(10, 11),
                gps_fix = True,
                aileron = 0,
                elevator = 0,
                throttle = 0
            )

            self.emit_signal()

            time.sleep(0.03)
    
    def parse_telemetry(self, payload, payload_length):
        self._tlm_packet.unpack(payload)

        self.bytes_read += payload_length + 3 # Add 3 because header
        elapsed = time.time() - self.prev_rate_calc_time
        if elapsed >= self.RATE_CALC_DT:
            self._rx_byte_rate = self.bytes_read / elapsed
            self.bytes_read = 0
            self.prev_rate_calc_time = time.time()
        
        self.emit_signal()

    def append_queue(self, payload):
        self._queue.add_payload(payload)

    def emit_signal(self):
        self.tlm_recv.emit({
            "latest_packet": self._tlm_packet,
            "queue_length": self._queue_len,
            "byte_rate": self._rx_byte_rate
        })
    
    def get_data(self):
        return self._tlm_packet