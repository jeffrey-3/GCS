# Plan coordinates in google maps, then import or type the coordinates into GCS
# Use PyQt drawing API to draw HUD on opencv pixmap
# You can test using flightgear

import pyqtgraph as pg
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import qdarktheme
import math
import time
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph

app = QApplication([])

pfd = PrimaryFlightDisplay(1000, 800)

class MyThread(QThread):
    frame_signal = pyqtSignal(QPixmap)

    def run(self):
        x = 0
        while True:
            roll = 5*math.cos(x/20)
            pitch = 30*math.sin(x/20)

            self.frame_signal.emit(pfd.update(pitch, roll, 100, 70, 10))
            
            x = x + 1
            time.sleep(0.05)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.create_ui_layout()
        self.add_ui()
        self.add_plot()
    
    def setup_window(self):
        qdarktheme.setup_theme()
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout)

    def create_ui_layout(self):
        self.ui_layout = QGridLayout()
        self.left_layout.addLayout(self.ui_layout)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_hud(self):
        self.hud_label = QLabel()
        self.left_layout.addWidget(self.hud_label)

        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)
        self.camera_thread.start()  

    @pyqtSlot(QPixmap)
    def setImage(self,image):
        self.hud_label.setPixmap(image)   
    
    def add_ui(self):
        self.state_label = QLabel("State<h1>Manual</h1>")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.state_label, 0, 0)

        self.flight_time_label = QLabel("Time<h1>00:00:00</h1>")
        self.flight_time_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.flight_time_label, 0, 1)

        self.voltage_label = QLabel("Voltage (V)<h1>11.04</h1>")
        self.voltage_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.voltage_label, 1, 0)

        self.current_label = QLabel("Current (A)<h1>30.46</h1>")
        self.current_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.current_label, 1, 1)

        self.rssi_label = QLabel("RSSI<h1>123</h1>")
        self.rssi_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.rssi_label, 2, 0)

        self.sats_label = QLabel("GPS Satellites<h1>12</h1>")
        self.sats_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.sats_label, 2, 1)

    def add_plot(self):
        self.map = Map()
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph)

main = MainWindow()
main.showFullScreen()
app.exec()