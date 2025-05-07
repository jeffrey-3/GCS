import time
import threading
import serial
import math
from PyQt5.QtCore import *
from aplink.aplink_messages import *
import random
from dataclasses import dataclass
from comms.base_radio import *

# Stm32 uses same architecture but flags for new_data instead of signal

class SerialRadio(BaseRadio):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    def __init__(self):
        super().__init__()
        self.aplink = APLink()
        self.ser = None
        self.port = None
        self.bytes_read_sum = 0 # Bytes read since last byte rate calculation
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
    
    def start(self, port):
        self.port = port

        try:
            self.ser = serial.Serial(port, 115200, timeout=1)
            threading.Thread(target=self._receive_thread, daemon=True).start()
            return True
        except:
            return False

    def transmit(self, bytes):
        self.ser.write(bytes)

    def _receive_thread(self):
        while True:
            byte = self.ser.read(1)
            result = self.aplink.parse_byte(ord(byte))
            if result is not None:
                payload, msg_id = result
                print(f"Radio Received msg_id: {msg_id}")

                self.bytes_read_sum += APLink().calculate_packet_size(len(payload))
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
                    self.vehicle_status_full_signal.emit(vehicle_status)
                elif msg_id == aplink_power.msg_id:
                    power = aplink_power()
                    power.unpack(payload)
                    self.power_signal.emit(power)
                elif msg_id == aplink_param_set.msg_id:
                    param_set = aplink_param_set()
                    param_set.unpack(payload)
                    self.param_set_signal.emit(param_set)
                elif msg_id == aplink_waypoints_ack.msg_id:
                    waypoints_ack = aplink_waypoints_ack()
                    waypoints_ack.unpack(payload)
                    self.waypoints_ack_signal.emit(waypoints_ack)
                elif msg_id == aplink_request_waypoint.msg_id:
                    request_waypoint = aplink_request_waypoint()
                    request_waypoint.unpack(payload)
                    self.request_waypoint_signal.emit(request_waypoint)