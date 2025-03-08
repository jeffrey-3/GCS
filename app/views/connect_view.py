from PyQt5.QtWidgets import *
import serial

class ConnectView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel("<h1>Connection</h1>"))

        # COM Port Selection
        self.com_port_label = QLabel("Select COM Port:")
        self.layout.addWidget(self.com_port_label)

        self.com_port_dropdown = QComboBox()
        self.layout.addWidget(self.com_port_dropdown)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh COM Ports")
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)