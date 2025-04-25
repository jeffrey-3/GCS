from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gcs import *

class DataView(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()
        self.gcs = gcs
        self.gcs.gps_raw_signal.connect(self.update_gps_raw)
        self.gcs.rx_byte_rate_signal.connect(self.update_byte_rate)
        self.gcs.power_signal.connect(self.update_power)

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
                label = self.layout.itemAtPosition(row, col).widget()
                w = self.height()
                small_font_size = int(0.1 * w)
                large_font_size = int(0.2 * w)
                
                label.setText(
                    f"<div align='center'>"
                    f"<span style='font-size:{small_font_size}px;'>{self.names[row][col]}</span><br>"
                    f"<b><span style='font-size:{large_font_size}px;'>{self.values[row][col]}</span></b>"
                    f"</div>"
                )

    
    def resizeEvent(self, event):
        self.render()