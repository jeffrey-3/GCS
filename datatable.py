from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Bar graphs:
# - Capacity consumed
# - Cell voltage
# - RSSI
# Data:
# - Time
# - GPS sats
# - State
# Map has distance

class DataTable(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.text = ["State", 
                     "Mission Time", 
                     "Battery Remaining", 
                     "Battery Voltage", 
                     "Battery Current", 
                     "Autopilot Current", 
                     "RSSI", 
                     "GPS Satellites", 
                     "Distance"]
        self.values = ["Manual", 
                       "00:00:00",
                       "00:00:00",
                       "11.04",
                       "30.46",
                       "30.46",
                       "123",
                       "12",
                       "123"]
        self.value_labels = []

        for row in range(3):
            for col in range(3):
                vbox = QVBoxLayout()
                vbox.setSpacing(2)

                label_small = QLabel(self.text[3*row + col], self)
                label_small.setStyleSheet("font-size: 30px;")  
                label_small.setAlignment(Qt.AlignCenter)
                label_small.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                label_large = QLabel(self.values[3*row + col], self)
                label_large.setStyleSheet("font-size: 60px; font-weight: bold;")
                label_large.setAlignment(Qt.AlignCenter)
                # label_large = QProgressBar()
                # label_large.setValue(50)
                label_large.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.value_labels.append(label_large)

                vbox.addWidget(label_small)
                vbox.addWidget(label_large)
                vbox.setAlignment(Qt.AlignCenter)

                self.layout.addLayout(vbox, row, col)
    
    def update(self, mode_id):
        state = "???"
        if mode_id == 0:
            state = "BOOT"
        elif mode_id == 2:
            state = "DIRECT"
        elif mode_id == 3:
            state = "STABILIZED"
        elif mode_id == 4:
            state = "READY"
        elif mode_id == 5:
            state = "TAKEOFF"
        elif mode_id == 6:
            state = "MISSION"
        elif mode_id == 7:
            state = "LAND"
        elif mode_id == 8:
            state = "FLARE"
        elif mode_id == 9:
            state = "SAFE"

        self.values = [state, 
                       "00:00:00",
                       "00:00:00",
                       "11.04",
                       "30.46",
                       "30.46",
                       "123",
                       "12",
                       "123"]
            
        for i in range(len(self.value_labels)):
            self.value_labels[i].setText(self.values[i])





















# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *

# # Bar graphs:
# # - Capacity consumed
# # - Cell voltage
# # - RSSI
# # Data:
# # - Time
# # - GPS sats
# # - State
# # Map has distance

# class DataTable(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.layout = QGridLayout()
#         self.setLayout(self.layout)

#         self.state_label =
#         self.layout.addWidget(QLabel("Test"), 0, 0)

#         self.layout.addWidget(QLabel("123"), 1, 0)

#         # self.state_label = QLabel("State<h1>Manual</h1>")
#         # # self.state_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.state_label, 0, 0)

#         # self.flight_time_label = QLabel("Mission Time<h1>00:00:00</h1>")
#         # # self.flight_time_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.flight_time_label, 0, 1)

#         # self.time_remaining_label = QLabel("Battery Remaining<h1>00:00:00</h1>")
#         # # self.time_remaining_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.time_remaining_label, 0, 2)

#         # self.voltage_label = QLabel("Battery Voltage (V)<h1>11.04</h1>")
#         # # self.voltage_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.voltage_label, 1, 0)

#         # self.current_label = QLabel("Battery Current (A)<h1>30.46</h1>")
#         # # self.current_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.current_label, 1, 1)

#         # self.ap_current_label = QLabel("Autopilot Current (mA)<h1>30.46</h1>")
#         # # self.ap_current_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.ap_current_label, 1, 2)

#         # self.rssi_label = QLabel("RSSI<h1>123</h1>")
#         # # self.rssi_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.rssi_label, 2, 0)

#         # self.sats_label = QLabel("GPS Satellites<h1>12</h1>")
#         # # self.sats_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.sats_label, 2, 1)

#         # self.distance_label = QLabel("Distance (m)<h1>123</h1>")
#         # # self.distance_label.setAlignment(Qt.AlignCenter)
#         # self.layout.addWidget(self.distance_label, 2, 2)
    
#     def update(self, mode_id):
#         state = "???"
#         if mode_id == 0:
#             state = "BOOT"
#         elif mode_id == 2:
#             state = "DIRECT"
#         elif mode_id == 3:
#             state = "STABILIZED"
#         elif mode_id == 4:
#             state = "READY"
#         elif mode_id == 5:
#             state = "TAKEOFF"
#         elif mode_id == 6:
#             state = "MISSION"
            
#         # self.state_label.setText("State<h1>" + state + "</h1>")