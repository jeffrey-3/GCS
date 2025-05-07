from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from gcs import *

class StateView(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()

        self.setStyleSheet("font-size: 40pt; font-weight: bold;")

        self.gcs = gcs
        self.gcs.vehicle_status_full_signal.connect(self.update_vehicle_status_full)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.state_label = QLabel("---")
        self.state_label
        self.state_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.state_label)

        self.time_label = QLabel("---")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        self.start_time = None
    
    def resizeEvent(self, event):
        self.setStyleSheet(f"font-size: {0.06 * self.size().width()}pt; font-weight: bold;")
    
    def update_vehicle_status_full(self, vehicle_status: aplink_vehicle_status_full):
        if vehicle_status.mode_id == MODE_ID.CONFIG:
            state = "CFG"
        elif vehicle_status.mode_id == MODE_ID.STARTUP:
            state = "ARM"
        elif vehicle_status.mode_id == MODE_ID.TAKEOFF:
            state = "TKO"
        elif vehicle_status.mode_id == MODE_ID.MISSION:
            state = "MIS"
            if not self.start_time:
                self.start_time = time.time()
        elif vehicle_status.mode_id == MODE_ID.LAND:
            state = "LND"
        elif vehicle_status.mode_id == MODE_ID.FLARE:
            state = "FLR"
        elif vehicle_status.mode_id == MODE_ID.MANUAL:
            state = "MAN"
        elif vehicle_status.mode_id == MODE_ID.FBW:
            state = "FBW"
        else:
            state = "ERR"
        
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            elapsed_hours = int(elapsed_time // 3600)
            elapsed_minutes = int((elapsed_time % 3600) // 60)
            elapsed_seconds = int(elapsed_time % 60)
            formatted_time = f"{elapsed_hours:02}:{elapsed_minutes:02}:{elapsed_seconds:02}"
        else:
            formatted_time = "00:00:00"
        
        self.state_label.setText(state)
        self.time_label.setText(formatted_time)