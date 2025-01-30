from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DataTable(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.state_label = QLabel("State<h1>Manual</h1>")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.state_label, 0, 0)

        self.flight_time_label = QLabel("Mission Time<h1>00:00:00</h1>")
        self.flight_time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.flight_time_label, 0, 1)

        self.time_remaining_label = QLabel("Battery Remaining<h1>00:00:00</h1>")
        self.time_remaining_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_remaining_label, 0, 2)

        self.voltage_label = QLabel("Battery Voltage (V)<h1>11.04</h1>")
        self.voltage_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.voltage_label, 1, 0)

        self.current_label = QLabel("Battery Current (A)<h1>30.46</h1>")
        self.current_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.current_label, 1, 1)

        self.ap_current_label = QLabel("Autopilot Current (mA)<h1>30.46</h1>")
        self.ap_current_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.ap_current_label, 1, 2)

        self.rssi_label = QLabel("RSSI<h1>123</h1>")
        self.rssi_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.rssi_label, 2, 0)

        self.sats_label = QLabel("GPS Satellites<h1>12</h1>")
        self.sats_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sats_label, 2, 1)

        self.distance_label = QLabel("Distance (m)<h1>123</h1>")
        self.distance_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.distance_label, 2, 2)