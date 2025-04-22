from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from radio import *

class DataView(QWidget):
    def __init__(self, radio: Radio):
        super().__init__()
        self.radio = radio
        self.radio.gps_raw_signal.connect(self.update_gps_raw)
        self.radio.rx_byte_rate_signal.connect(self.update_byte_rate)
        self.radio.power_signal.connect(self.update_power)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.names = [["GPS Fix", "GPS Sats", "Byte Rate"],
                      ["Voltage", "Current", "Used"]]
    
        self.values = [["---", "---", "---"],
                       ["---", "---", "---"]]

        for row in range(len(self.names)):
            for col in range(len(self.names[0])):
                self.layout.addWidget(QLabel(alignment=Qt.AlignCenter), row, col)
        
        self.render()
    
    def update_power(self, power: aplink_power):
        self.values[1][0] = round(power.batt_volt, 1)
        self.values[1][1] = round(power.batt_curr, 1)
        self.values[1][2] = int(power.batt_used)

    def update_gps_raw(self, gps_raw: aplink_gps_raw):
        self.values[0][0] = "YES" if gps_raw.fix else "NO"
        self.values[0][1] = gps_raw.sats
        self.render()
    
    def update_byte_rate(self, byte_rate: int):
        self.values[0][2] = byte_rate
        self.render()
    
    def render(self):
        for row in range(len(self.names)):
            for col in range(len(self.names[0])):
                self.layout.itemAtPosition(row, col).widget().setText(
                    f"<div style='font-size: 50px;'>{self.names[row][col]}</div>"
                    f"<div style='font-size: 100px; font-weight: bold;'>{self.values[row][col]}</div>"
                )