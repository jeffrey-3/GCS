from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import math
from app.utils.utils import calculate_displacement_meters
import time

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

        self.start_time = time.time()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.text = ["State", 
                     "Mission Time", 
                     "Home Distance",
                     "GPS Fix", 
                     "GPS Sats", 
                     "Packet Rate",
                     "Cell Voltage", 
                     "Batt Current", 
                     "Capacity Consumed"]
        self.value_labels = []

        for row in range(3):
            for col in range(3):
                vbox = QVBoxLayout()
                vbox.setSpacing(2)

                label_small = QLabel(self.text[3*row + col], self)
                label_small.setStyleSheet("font-size: 30px;")  
                label_small.setAlignment(Qt.AlignCenter)
                label_small.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                label_large = QLabel("Value", self)
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
    
    def update(self, flight_data):
        if flight_data.mode_id == 0:
            state = "CONFIG"
        elif flight_data.mode_id == 1:
            state = "STARTUP"
        elif flight_data.mode_id == 2:
            state = "TAKEOFF"
        elif flight_data.mode_id == 3:
            state = "MISSION"
        elif flight_data.mode_id == 4:
            state = "LAND"
        elif flight_data.mode_id == 5:
            state = "FLARE"
        elif flight_data.mode_id == 6:
            state = "TOUCHDOWN"
        elif flight_data.mode_id == 7:
            state = "DIRECT"
        elif flight_data.mode_id == 8:
            state = "STAB"
        else:
            state = "UNKNOWN"
        
        elapsed_time = time.time() - self.start_time
        elapsed_hours = int(elapsed_time // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)
        formatted_time = f"{elapsed_hours:02}:{elapsed_minutes:02}:{elapsed_seconds:02}"

        pos = calculate_displacement_meters(flight_data.lat, flight_data.lon, flight_data.center_lat, flight_data.center_lon)
        dist = math.sqrt(pos[0]**2 + pos[1]**2) # Use total distance instead of displacement

        values = [state, 
                  formatted_time,
                  f"{dist:.0f}",
                  str(flight_data.gps_fix),
                  str(flight_data.sats),
                  f"{flight_data.packet_rate:.0f}",
                  f"{flight_data.cell_voltage:.2f}",
                  f"{flight_data.current:.1f}",
                  f"{flight_data.capacity_consumed:.0f}"]
        for i in range(len(self.value_labels)):
            self.value_labels[i].setText(values[i])