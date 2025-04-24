import time
import threading
import serial
import math
from PyQt5.QtCore import *
from aplink.aplink_messages import *
from typing import List
import array
import random
from dataclasses import dataclass

# Single poll function with signals for everything, then functions that listen for handling acks
# This way, you don't have to toggle poll on and off

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float

@dataclass
class Parameter:
    name: str
    value: float
    type: str

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    cal_sensors_signal = pyqtSignal(aplink_cal_sensors)
    gps_raw_signal = pyqtSignal(aplink_gps_raw)
    vehicle_status_full_signal = pyqtSignal(aplink_vehicle_status_full)
    power_signal = pyqtSignal(aplink_power)

    rx_byte_rate_signal = pyqtSignal(int)

    waypoints_updated = pyqtSignal(list)
    params_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.aplink = APLink()
        self.ser = None
        self.port = None
        self.bytes_read_sum = 0 # Bytes read since last byte rate calculation
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
        self.waypoints: List[Waypoint] = []
        self.params: List[Parameter] = []
        self.get_telemetry_active = True
    
    def start(self, port):
        self.port = port
        
        if port == 'Testing':
            threading.Thread(target=self.testing_thread, daemon=True).start()
        else:
            try:
                self.ser = serial.Serial(port, 115200, timeout=1)
                threading.Thread(target=self.get_telemetry, daemon=True).start()
            except:
                return False

        return True

    def get_telemetry(self):
        while True:
            if self.get_telemetry_active:
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

                    if msg_id == aplink_cal_sensors.msg_id:
                        cal_sensors = aplink_cal_sensors()
                        cal_sensors.unpack(payload)
                        self.cal_sensors_signal.emit(vehicle_status)
                    elif msg_id == aplink_vehicle_status_full.msg_id:
                        vehicle_status = aplink_vehicle_status_full()
                        vehicle_status.unpack(payload)
                        self.vfr_hud_signal.emit(vehicle_status)

                    return payload, msg_id
            else:
                time.sleep(0.01)
                    
    def send_waypoints(self, waypoints: List[Waypoint]):
        self.waypoints = waypoints

        if self.port == "Testing":
            self.waypoints_updated.emit(waypoints)
            return True
        
        self.get_telemetry_active = False  # Stop background polling

        # Notify plane that GCS is about to send waypoints
        self.ser.write(aplink_waypoints_count().pack(len(self.waypoints)))

        # Listen for plane to request each waypoint
        timeout_sec = 1
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            byte = self.ser.read(1)
            result = self.aplink.parse_byte(byte)
            if result is not None:
                payload, msg_id = result

                if msg_id == aplink_request_waypoint.msg_id:
                    request_waypoint = aplink_request_waypoint()
                    request_waypoint.unpack(payload)

                    # If plane requests waypoint, send the waypoint
                    self.ser.write(aplink_waypoint().pack(
                        self.waypoints[request_waypoint.index].lat * 1e7, 
                        self.waypoints[request_waypoint.index].lon * 1e7, 
                        self.waypoints[request_waypoint.index].alt
                    ))

                    start_time = time.time() # Reset timeout
                elif msg_id == aplink_waypoints_ack.msg_id:
                    # Exit when plane uses waypoints_count to confirm all waypoints have been loaded
                    ack = aplink_waypoints_ack()
                    ack.unpack(payload)
                    self.get_telemetry_active = True  # Resume background polling
                    self.waypoints_updated.emit(waypoints)
                    return True
                
        self.get_telemetry_active = True  # Resume background polling if timeout
        return False
        
    # Send param_set and plane replies with the same param_set to confirm
    def send_params(self, params: List[Parameter]):
        self.params = params

        if self.port == "Testing":
            self.params_updated.emit(self.params)
            return True

        self.get_telemetry_active = False  # Stop background polling
        for param in self.params:
            param_name = param.name.ljust(16, '\x00')[16:].encode('utf-8') # Convert to 16-byte char array
            param_value = None
            param_type = None
            if param.name == "f":
                param_type = PARAM_TYPE.FLOAT
                param_value = array.array('B', struct.pack('=f', param.value))
            elif param.name == "i":
                param_type = PARAM_TYPE.INT32
                param_value = array.array('B', struct.pack('=i', param.value))

            self.ser.write(aplink_param_set().pack(param_name, param_value, param_type))

            timeout_sec = 1
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                byte = self.ser.read(1)
                result = self.aplink.parse_byte(byte)
                if result is not None:
                    payload, msg_id = result
                    if msg_id == aplink_param_set.msg_id:
                        start_time = time.time()
                        continue
        
            return False

        self.get_telemetry_active = True  # Resume background polling
        self.params_updated.emit(self.params)
        return True

    def testing_thread(self):
        while True:
            t = time.time()

            lat = 43.878960 + 0.001 * math.sin(t / 2)
            lon = -79.413383 + 0.001 * math.cos(t / 2)

            vehicle_status_full = aplink_vehicle_status_full()
            vehicle_status_full.pitch = 10 * math.sin(t / 2)
            vehicle_status_full.roll = 10 * math.sin(t / 2)
            vehicle_status_full.yaw = 10 * math.sin(t / 2)
            vehicle_status_full.alt = 15 + 10 * math.sin(t / 2)
            vehicle_status_full.spd = 15 + 10 * math.sin(t / 2)
            vehicle_status_full.lat = lat
            vehicle_status_full.lon = lon
            vehicle_status_full.current_waypoint = 1
            vehicle_status_full.mode_id = MODE_ID.TAKEOFF
            self.vehicle_status_full_signal.emit(vehicle_status_full)

            gps_raw = aplink_gps_raw()
            gps_raw.lat = lat
            gps_raw.lon = lon
            gps_raw.fix = True
            gps_raw.sats = random.randint(9,12)
            self.gps_raw_signal.emit(gps_raw)

            power = aplink_power()
            power.batt_volt = 12.67
            power.batt_curr = 11.4
            power.batt_used = 607
            self.power_signal.emit(power)

            self.rx_byte_rate_signal.emit(random.randint(900, 1500))

            time.sleep(0.02)