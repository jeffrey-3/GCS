from PyQt5.QtWidgets import *
import serial

class ConnectView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Connection</h1>"))

        # COM Port Selection
        self.com_port_label = QLabel("Select COM Port:")
        self.com_port_label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.com_port_label)

        self.com_port_dropdown = QComboBox()
        self.com_port_dropdown.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.com_port_dropdown)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh COM Ports")
        self.refresh_button.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.refresh_button)

        self.layout.addStretch()