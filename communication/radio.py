import time
import threading
import serial
import random
from lib.cobs import cobs
import math
from PyQt5.QtCore import *
from communication.aplink.aplink import APLink
from communication.aplink.messages.cal_sensors import CalSensors
from communication.aplink.messages.vfr_hud import VFRHUD
from communication.aplink.messages.nav_display import NavDisplay

class Radio(QObject):
    RATE_CALC_DT = 1 # Delta time to calculate received byte rate

    cal_sensors_signal = pyqtSignal(float, float, float, float, float, float, float, float, float)
    vfr_hud_signal = pyqtSignal(float, float, float, float, float)
    nav_display_signal = pyqtSignal(float, float, int)
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
                    self.cal_sensors_signal.emit(
                        cal_sensors.ax, cal_sensors.ay, cal_sensors.az, 
                        cal_sensors.gx, cal_sensors.gy, cal_sensors.gz,
                        cal_sensors.mx, cal_sensors.my, cal_sensors.mz
                    )
                elif msg_id == VFRHUD.MSG_ID:
                    vfr_hud = VFRHUD()
                    vfr_hud.unpack(payload)
                    print(vfr_hud.alt)
                    self.vfr_hud_signal.emit(
                        vfr_hud.roll, 
                        vfr_hud.pitch, 
                        vfr_hud.yaw
                    )
                elif msg_id == NavDisplay.MSG_ID:
                    nav_display = NavDisplay()
                    nav_display.unpack(payload)
                    self.nav_display_signal.emit(
                        nav_display.pos_est_north,
                        nav_display.pos_est_east,
                        nav_display.waypoint_index
                    )
    
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