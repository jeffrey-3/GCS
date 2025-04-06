import time
import threading
import serial
import random
from lib.cobs import cobs
import math
from PyQt5.QtCore import *
from aplink.aplink import APLink
from aplink.messages.cal_sensors import CalSensors
from aplink.messages.vfr_hud import VFRHUD
from aplink.messages.nav_display import NavDisplay

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    cal_sensors_signal = pyqtSignal(CalSensors)
    vfr_hud_signal = pyqtSignal(VFRHUD)
    nav_display_signal = pyqtSignal(NavDisplay)
    rx_byte_rate_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.aplink = APLink()
        self.ser = None
        self.port = None
        self.bytes_read_sum = 0 # Bytes read since last byte rate calculation
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
    
    def start(self, port):
        if port != 'Testing':
            try:
                self.ser = serial.Serial(port, 115200, timeout=1000)
            except:
                return False
            self.port = port
            threading.Thread(target=self.receive_thread, daemon=True).start()
            return True
        else:
            threading.Thread(target=self.testing_thread, daemon=True).start()
            return True

    def transmit(self):
        self.ser.write(self.payload_to_packet(self._queue[0]))
    
    def receive_thread(self):
        while True:
            byte = self.ser.read(1)
            result = self.aplink.parse_byte(byte)
            if result is not None:
                payload, msg_id = result

                self.bytes_read_sum += APLink.calculate_packet_size(len(payload))
                elapsed = time.time() - self.prev_rate_calc_time
                if elapsed >= self.RATE_CALC_DT:
                    self.rx_byte_rate_signal.emit(self.bytes_read_sum / elapsed)
                    self.bytes_read_sum = 0
                    self.prev_rate_calc_time = time.time()

                if msg_id == CalSensors.MSG_ID:
                    cal_sensors = CalSensors()
                    cal_sensors.unpack(payload)
                    print(cal_sensors.az)
                    self.cal_sensors_signal.emit([
                        cal_sensors.ax, cal_sensors.ay, cal_sensors.az, 
                        cal_sensors.gx, cal_sensors.gy, cal_sensors.gz,
                        cal_sensors.mx, cal_sensors.my, cal_sensors.mz
                    ])
                elif msg_id == VFRHUD.MSG_ID:
                    vfr_hud = VFRHUD()
                    vfr_hud.unpack(payload)
                    print(vfr_hud.alt)
                    self.vfr_hud_signal.emit({
                        "roll": vfr_hud.roll, 
                        "pitch": vfr_hud.pitch, 
                        "yaw:": vfr_hud.yaw
                    })
    
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

    def payload_to_packet(self, payload):
        return bytes([0x00]) + bytes([payload.struct_size]) + bytes([payload.msg_id]) + cobs.encode(payload.pack())

    def add_payload_to_queue(self, payload):
        self._queue.append(payload)
    
    def get_data(self):
        return self._tlm_payload
