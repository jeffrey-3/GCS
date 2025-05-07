import time
import threading
import serial
import math
from PyQt5.QtCore import *
from aplink.aplink_messages import *
import random
from dataclasses import dataclass
from comms.base_radio import *

class TestingRadio(BaseRadio):
    def __init__(self):
        super().__init__()
        self.aplink = APLink()
    
    def start(self, port):
        threading.Thread(target=self._receive_thread, daemon=True).start()
        return True

    def transmit(self, bytes):
        # Simulate receiving messages
        time.sleep(0.1)
        result = APLink().unpack(bytes)
        if result is not None:
            payload, msg_id = result
            if msg_id == aplink_waypoints_count.msg_id:
                waypoints_ack = aplink_waypoints_ack()
                waypoints_ack.success = True
                self.waypoints_ack_signal.emit(waypoints_ack)
            elif msg_id == aplink_param_set.msg_id:
                self.param_set_signal.emit(aplink_param_set())       
    
    def _receive_thread(self):
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
            vehicle_status_full.mode_id = MODE_ID.MISSION
            self.vehicle_status_full_signal.emit(vehicle_status_full)

            gps_raw = aplink_gps_raw()
            gps_raw.lat = lat
            gps_raw.lon = lon
            gps_raw.fix = True
            gps_raw.sats = random.randint(9,12)
            self.gps_raw_signal.emit(gps_raw)

            power = aplink_power()
            power.batt_volt = 3.8
            power.batt_curr = 11.4
            power.batt_used = 607
            self.power_signal.emit(power)

            cal_sensors = aplink_cal_sensors()
            cal_sensors.ax = -0.1 * math.sin(t)
            cal_sensors.ay = 0.1 * math.sin(t)
            cal_sensors.az = 1 + 0.1 * math.sin(t)
            cal_sensors.gx = 0.1 * math.sin(t)
            cal_sensors.gy = 0.1 * math.sin(t)
            cal_sensors.gz = 0.1 * math.sin(t)
            self.cal_sensors_signal.emit(cal_sensors)

            self.rx_byte_rate_signal.emit(random.randint(900, 1500))

            time.sleep(0.02)