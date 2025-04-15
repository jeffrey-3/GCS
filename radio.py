import time
import threading
import serial
import math
from PyQt5.QtCore import *
from aplink.aplink_messages import *
from dataclasses import dataclass

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    cal_sensors_signal = pyqtSignal(float, float, float, float, float, float, float, float, float)
    vfr_hud_signal = pyqtSignal(float, float, float, float, float)
    nav_display_signal = pyqtSignal(float, float, int)
    rx_byte_rate_signal = pyqtSignal(float)
    request_waypoint_signal = pyqtSignal(int)

    waypoints_updated = pyqtSignal(list)
    map_clicked_signal = pyqtSignal(tuple)
    params_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.aplink = APLink()
        self.ser = None
        self.port = None
        self.connected = False
        self.bytes_read_sum = 0 # Bytes read since last byte rate calculation
        self.prev_rate_calc_time = time.time() # Time of last byte rate calculation
        self.waypoints = []
    
    def update_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.waypoints_updated.emit(waypoints)
    
    def map_clicked(self, pos):
        self.map_clicked_signal.emit(pos)
    
    def get_waypoints(self):
        return self.waypoints
    
    def start(self, port):
        self.port = port
        
        if port != 'Testing':
            try:
                self.ser = serial.Serial(port, 115200, timeout=1000)
            except:
                return False
            
            threading.Thread(target=self.receive_thread, daemon=True).start()
        else:
            threading.Thread(target=self.testing_thread, daemon=True).start()
    
        self.connected = True

        return True
    
    def upload_waypoints(self, waypoints):
        if self.port == "Testing":
            return True

        try:
            self.ser.write(aplink_waypoints_count().pack(len(waypoints)))
            return True
        except:
            return False

    def send_waypoint(self, waypoint):
        self.ser.write(aplink_waypoint().pack(waypoint.lat, waypoint.lon, waypoint.alt))
    
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

                if msg_id == aplink_cal_sensors.msg_id:
                    cal_sensors = aplink_cal_sensors()
                    cal_sensors.unpack(payload)
                    print(cal_sensors.az)
                    self.cal_sensors_signal.emit(
                        cal_sensors.ax, cal_sensors.ay, cal_sensors.az, 
                        cal_sensors.gx, cal_sensors.gy, cal_sensors.gz,
                        cal_sensors.mx, cal_sensors.my, cal_sensors.mz
                    )
                elif msg_id == aplink_vfr_hud.msg_id:
                    vfr_hud = aplink_vfr_hud()
                    vfr_hud.unpack(payload)
                    print(vfr_hud.alt)
                    self.vfr_hud_signal.emit(
                        vfr_hud.roll, 
                        vfr_hud.pitch, 
                        vfr_hud.yaw
                    )
                elif msg_id == aplink_nav_display.msg_id:
                    nav_display = aplink_nav_display()
                    nav_display.unpack(payload)
                    self.nav_display_signal.emit(
                        nav_display.pos_est_north,
                        nav_display.pos_est_east,
                        nav_display.waypoint_index
                    )
                elif msg_id == aplink_request_waypoint.msg_id:
                    request_waypoint = aplink_request_waypoint()
                    request_waypoint.unpack(payload)
                    self.request_waypoint_signal.emit(request_waypoint.index)
    
    def testing_thread(self):
        while True:
            t = time.time()

            self.nav_display_signal.emit(
                100 * math.sin(t / 2),
                100 * math.cos(t / 2),
                2
            )

            self.vfr_hud_signal.emit(
                10 * math.sin(t / 2),
                10 * math.sin(t / 2),
                10 * math.sin(t / 2),
                15 + 10 * math.sin(t / 2),
                15 + 10 * math.sin(t / 2)
            )

            time.sleep(0.02)        