from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from gcs import *

# Accelerometer you hold still at orientations, magnetometer you rotate around freely

# https://youtu.be/vRWixUAko4g?si=wXK4oEjmrIuvR3V8

class Calibration(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()
        self.gcs = gcs
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Gyroscope</h1>"))

        self.layout.addWidget(QLabel("GYR_OFF_X: -\nGYR_OFF_Y: -\nGYR_OFF_Z: -"))

        self.layout.addWidget(QPushButton("Start"))

        self.layout.addWidget(QLabel("<h1>Accelerometer</h1>"))

        label = QLabel("ACC_OFF_X: -\nACC_OFF_Y: -\nACC_OFF_Z: -")
        label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(label)

        self.position_label = QLabel("-")
        self.position_label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.position_label)

        self.next_btn = QPushButton("Start")
        self.next_btn.setStyleSheet("font-size: 12pt;")
        self.next_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.next_btn.clicked.connect(self.next_position_pressed)
        self.layout.addWidget(self.next_btn)

        self.layout.addWidget(QLabel("<h1>Magnetometer</h1>"))

        self.layout.addWidget(QLabel("MAG_HI_X: -\nGYR_HI_Y: -\nGYR_HI_Z: -\nMAG_SI_X: -\nGYR_SI_Y: -\nGYR_SI_Z: -"))

        self.layout.addWidget(QPushButton("Start"))

        self.layout.addStretch()

        self.position = 0

        self.gcs.cal_sensors_signal.connect(self.update_cal_sensors)
    
    def next_position_pressed(self):
        if self.position == 6:
            self.position = 0
            self.position_label.setText("-")
            self.next_btn.setText("Start")

            # Calculate offsets here
        else:
            positions = ["LEVEL", "ROLL RIGHT", "ROLL LEFT", "NOSE UP", "NOSE DOWN", "INVERTED"]

            self.position_label.setText("Place the vehicle " + positions[self.position])
            self.position += 1
            self.next_btn.setText("Continue")
    
    def update_cal_sensors(self, aplink_cal_sensors: aplink_cal_sensors):
        # print(aplink_cal_sensors.ax)
        return