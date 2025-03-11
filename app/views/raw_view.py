from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class RawView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        # self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(self.label)
    
    # Use table?
    def update(self, flight_data):
        self.label.setText(f"Queue: {flight_data.queue_len}\nGNSS Lat: {flight_data.lat:.7f}\nGNSS Lon: {flight_data.lon:.7f}")