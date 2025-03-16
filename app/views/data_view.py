from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DataView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.names = [["GPS Fix", "GPS Sats", "Byte Rate"],
                      ["Voltage", "Current", "Used"]]

        for row in range(len(self.names)):
            for col in range(len(self.names[0])):
                self.layout.addWidget(QLabel(alignment=Qt.AlignCenter), row, col)

    def update(self, gps_fix, gps_sats, byte_rate, cell_voltage, battery_current, capacity_consumed):
        values = [["YES" if gps_fix else "NO", str(gps_sats), f"{byte_rate:.0f}"],
                  [f"{cell_voltage:.2f}", f"{battery_current:.1f}", f"{capacity_consumed:.0f}"]]
        
        for row in range(len(self.names)):
            for col in range(len(self.names[0])):
                self.layout.itemAtPosition(row, col).widget().setText(
                    f"<div style='font-size: 50px;'>{self.names[row][col]}</div>"
                    f"<div style='font-size: 100px; font-weight: bold;'>{values[row][col]}</div>"
                )