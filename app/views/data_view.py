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

    def update(self, flight_data):
        values = [["YES" if flight_data.gps_fix else "NO", str(flight_data.sats), f"{flight_data.packet_rate:.0f}"],
                  [f"{flight_data.cell_voltage:.2f}", f"{flight_data.current:.1f}", f"{flight_data.capacity_consumed:.0f}"]]
        
        for row in range(len(self.names)):
            for col in range(len(self.names[0])):
                self.layout.itemAtPosition(row, col).widget().setText(
                    f"<div style='font-size: 50px;'>{self.names[row][col]}</div>"
                    f"<div style='font-size: 100px; font-weight: bold;'>{values[row][col]}</div>"
                )