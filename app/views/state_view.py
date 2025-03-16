from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time

class StateView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.state_label = QLabel("---")
        self.state_label.setStyleSheet("font-size: 40pt; font-weight: bold;")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.state_label)

        self.time_label = QLabel("---")
        self.time_label.setStyleSheet("font-size: 40pt; font-weight: bold;")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        self.start_time = None
    
    def update(self, data):
        flight_data = data["latest_packet"]

        if not self.start_time:
            self.start_time = time.time()

        if flight_data.data.mode_id == 0:
            state = "CONFIG"
        elif flight_data.data.mode_id == 1:
            state = "STARTUP"
        elif flight_data.data.mode_id == 2:
            state = "TAKEOFF"
        elif flight_data.data.mode_id == 3:
            state = "MISSION"
        elif flight_data.data.mode_id == 4:
            state = "LAND"
        elif flight_data.data.mode_id == 5:
            state = "FLARE"
        elif flight_data.data.mode_id == 6:
            state = "CONTACT"
        elif flight_data.data.mode_id == 7:
            state = "DIRECT"
        elif flight_data.data.mode_id == 8:
            state = "STAB"
        else:
            state = f"UNKNOWN: {flight_data.data.mode_id}"
        
        elapsed_time = time.time() - self.start_time
        elapsed_hours = int(elapsed_time // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)
        formatted_time = f"{elapsed_hours:02}:{elapsed_minutes:02}:{elapsed_seconds:02}"
        
        self.state_label.setText(state)
        self.time_label.setText(formatted_time)