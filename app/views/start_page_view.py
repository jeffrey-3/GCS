from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StartPageView(QWidget):
    new_mission_signal = pyqtSignal()
    reconnect_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        title = QLabel("UAV Ground Control")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.layout.addStretch()

        self.new_mission_btn = QPushButton("New Mission")
        self.new_mission_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.new_mission_btn.clicked.connect(self.new_mission_signal.emit)
        self.layout.addWidget(self.new_mission_btn)

        self.layout.addStretch()

        self.reconnect_btn = QPushButton("Reconnect")
        self.reconnect_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.reconnect_btn.clicked.connect(self.reconnect_signal.emit)
        self.layout.addWidget(self.reconnect_btn)

        self.layout.addStretch()

        self.download_logs_btn = QPushButton("Download Logs")
        self.download_logs_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        # self.download_logs_btn.clicked.connect(self.reconnect_signal.emit)
        self.layout.addWidget(self.download_logs_btn)

        # Calibrate all sensors at once, you don't have to use the values tho
        # Three calibration buttons for gyro, accel, mag
        # When clicked, it calibrates
        # In calibration mode, it sends command to put plane in calibration mode
        self.calib_btn = QPushButton("Sensor Calibration")
        self.calib_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        # self.download_logs_btn.clicked.connect(self.reconnect_signal.emit)
        self.layout.addWidget(self.calib_btn)

        self.setLayout(self.layout)