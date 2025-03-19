import time
import threading
import serial
import random
from lib.cobs import cobs
import math
from PyQt5.QtCore import *
from communication.binary_struct import *

# Send payload to radio
# Radio adds header, COBS, and checksum and sends it through
# Radio receives packet and decodes into payload 

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate
    TRANSMIT_DT = 0.5 # Delta time to transmit packets

    tlm_recv = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._tlm_payload = TelemetryPayload()
        self._queue = [] # Queue to store payloads awaiting transmission
        self._rx_byte_rate = 0 # Received byte rate
        self.ser = None
        self.port = None
        self.bytes_read = 0 # Bytes read since last byte rate calculation
        self.prev_send_time = time.time() # Time of last transmit
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
    
    def start(self, port):
        self.port = port
        if port != 'Testing':
            try:
                self.ser = serial.Serial(port, 115200, timeout=1000)
            except:
                return False
        
            threading.Thread(target=self.transmit_thread, daemon=True).start()
            threading.Thread(target=self.receive_thread, daemon=True).start()

            return True
        else:
            threading.Thread(target=self.testing_thread, daemon=True).start()

            return True

    def transmit_thread(self):
        while True:
            elapsed_time = time.time() - self.prev_send_time
            if len(self._queue.queue) > 0 and elapsed_time > self.TRANSMIT_DT:
                self.ser.write(
                    self.payload_to_packet(self._queue[0])
                )
                self._queue.remove(self._queue[0])
                self.prev_send_time = time.time()
    
    def receive_thread(self):
        while True:
            # Find start byte
            packet = self.ser.read(1)

            # Detect start byte
            if packet == b'\x00':
                # Get length byte
                payload_length = self.ser.read(1)
                packet.extend(payload_length)

                # Get message ID
                msg_id = self.ser.read(1)
                packet.extend(msg_id)
        
                # Read payload and COBS byte
                payload_cobs = self.ser.read(int.from_bytes(payload_length, 'little') + 1)
                packet.extend(payload_cobs)

                # Decode to remove COBS byte and get payload
                payload = cobs.decode(payload_cobs)

                # Figure out what type of payload from message ID
                if int.from_bytes(msg_id, 'little') == TelemetryPayload().msg_id: 
                    # Telemetry payload
                    self.parse_telemetry(payload, int.from_bytes(payload_length, 'little'))
                else:
                    # If acknowledgement received, remove from queue
                    if payload in self._queue:
                        self._queue.remove(payload)
    
    def testing_thread(self):
        while True:
            t = time.time()
            self._tlm_payload.set_data(
                roll = 10 * math.cos(t),
                pitch = 10 * math.sin(t),
                heading = 180 + 180*math.sin(t/5),
                altitude = 20 - 5 * math.sin(t),
                airspeed = 10 - 5 * math.cos(t),
                altitude_setpoint = 0,
                gnss_latitude = 43.878258 + 0.002 * math.sin(t/6),
                gnss_longitude = -79.413123 + 0.002 * math.cos(t/6),
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

            time.sleep(0.02)
    
    def parse_telemetry(self, payload, payload_length):
        self._tlm_payload.unpack(payload)

        self.bytes_read += payload_length + 3 # Add 3 because header
        elapsed = time.time() - self.prev_rate_calc_time
        if elapsed >= self.RATE_CALC_DT:
            self._rx_byte_rate = self.bytes_read / elapsed
            self.bytes_read = 0
            self.prev_rate_calc_time = time.time()
        
        self.emit_signal()

    def payload_to_packet(self, payload):
        return bytes([0x00]) + bytes([len(payload)]) + bytes([payload.id]) + cobs.encode(payload.pack)

    def add_payload_to_queue(self, payload):
        self._queue.append(payload)

    def emit_signal(self):
        self.tlm_recv.emit({
            "latest_payload": self._tlm_payload,
            "queue_length": len(self._queue),
            "byte_rate": self._rx_byte_rate
        })
    
    def get_data(self):
        return self._tlm_payload
