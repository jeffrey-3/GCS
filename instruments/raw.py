from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from radio import *

class RawTable(QWidget):
    def __init__(self, names, units):
        super().__init__()

        self.names = names
        self.units = units

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.rows = len(self.names)

        for row in range(self.rows):
            self.layout.addWidget(QLabel(self.names[row], styleSheet="font-size: 12pt;"), row, 0)
            self.layout.addWidget(QLabel("-", styleSheet="font-size: 12pt;"), row, 1)
            self.layout.addWidget(QLabel(self.units[row], styleSheet="font-size: 12pt;"), row, 2)
    
    def update(self, values):
        for row in range(self.rows):
            self.layout.itemAtPosition(row, 1).widget().setText(values[row])

class RawView(QScrollArea):
    def __init__(self, radio: Radio):
        super().__init__()

        self.radio = radio
        self.radio.vehicle_status_full_signal.connect(self.vehicle_status_full_update)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>GNSS</h1>"))

        self.gnss_table = RawTable(["Lat", "Lon", "North", "East"], ["deg", "deg", "m", "m"])
        self.layout.addWidget(self.gnss_table)

        self.layout.addWidget(QLabel("<h1>Telemetry</h1>"))

        self.tlm_table = RawTable(["Queue Length", "Timed Out Packets", "Rejected Packets"], ["", "", ""])
        self.layout.addWidget(self.tlm_table)

        self.layout.addWidget(QLabel("<h1>Navigation</h1>"))

        self.nav_table = RawTable(["Position North", "Position East", "Altitude", "Groundspeed"], ["m", "m", "m", "m/s"])
        self.layout.addWidget(self.nav_table)

        self.layout.addWidget(QLabel("<h1>AHRS</h1>"))

        self.ahrs_table = RawTable(["Roll", "Pitch", "Heading"], ["deg", "deg", "deg"])
        self.layout.addWidget(self.ahrs_table)

        self.layout.addWidget(QLabel("<h1>RC Transmitter</h1>"))

        self.rc_table = RawTable(["Aileron", "Elevator", "Throttle"], ["", "", ""])
        self.layout.addWidget(self.rc_table)

        self.layout.addStretch()

        container = QWidget()
        container.setLayout(self.layout)
        self.setWidget(container)
    
    def vehicle_status_full_update(self, vehicle_status: aplink_vehicle_status_full):
        self.ahrs_table.update([str(round(vehicle_status.roll, 2)),
                               str(round(vehicle_status.pitch, 2)),
                               str(round(vehicle_status.yaw, 2))])

# Maybe auto generate based on packet names