import time
import threading
import serial
import math
from PyQt5.QtCore import *
from aplink.aplink_messages import *
import json

# IF you want to seperate GCS and radio, have radio library which GCS includes

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    cal_sensors_signal = pyqtSignal(list)
    vehicle_status_full_signal = pyqtSignal(aplink_vehicle_status_full)

    rx_byte_rate_signal = pyqtSignal(float)

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
        self.params = []
    
    def update_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.save_last_flightplan()
        self.waypoints_updated.emit(waypoints)
    
    def update_params(self, params):
        self.params = params
        self.save_params(params)
    
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
                    
                    self.ser.write(aplink_waypoint().pack(self.waypoints[request_waypoint.index].lat, 
                                                          self.waypoints[request_waypoint.index].lon, 
                                                          self.waypoints[request_waypoint.index].alt))
    
    def testing_thread(self):
        while True:
            t = time.time()

            vehicle_status_full = aplink_vehicle_status_full()
            vehicle_status_full.pitch = 10 * math.sin(t / 2)
            vehicle_status_full.roll = 10 * math.sin(t / 2)
            vehicle_status_full.yaw = 10 * math.sin(t / 2)
            vehicle_status_full.alt = 15 + 10 * math.sin(t / 2)
            vehicle_status_full.spd = 15 + 10 * math.sin(t / 2)
            vehicle_status_full.lat = 43.878960 + 0.001 * math.sin(t / 2)
            vehicle_status_full.lon = -79.413383 + 0.001 * math.cos(t / 2)
            self.vehicle_status_full_signal.emit(vehicle_status_full)

            time.sleep(0.02)        
    
    def save_params(self, params):
        json_data = [
            {"name": param.name, "value": param.value, "type": param.type} 
            for param in params
        ]

        f = open("resources/last_params.json", 'w')
        json.dump(json_data, f, indent=4)

        print("Last params saved")
    
    def save_last_flightplan(self):
        json_data = [
            {"lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
            for wp in self.waypoints
        ]

        f = open("resources/last_flightplan.json", "w")
        json.dump(json_data, f, indent=4)

        print("Last flight plan saved")