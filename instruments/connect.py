import serial.tools.list_ports
from PyQt5.QtWidgets import *

class ConnectView(QWidget):
    def __init__(self, radio):
        super().__init__()
        self.radio = radio
        self.create()
        self.refresh_button.clicked.connect(self.refresh_com_ports)
        self.connect_button.clicked.connect(self.connect)

        # Initialize
        self.refresh_com_ports()

    def create(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Connection</h1>"))

        # COM Port Selection
        self.com_port_label = QLabel("Select COM Port:")
        self.com_port_label.setStyleSheet("font-size: 12pt;")
        self.com_port_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.com_port_label)

        self.com_port_dropdown = QComboBox()
        self.com_port_dropdown.setStyleSheet("font-size: 12pt;")
        self.com_port_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.com_port_dropdown)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh COM Ports")
        self.refresh_button.setStyleSheet("font-size: 12pt;")
        self.refresh_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.refresh_button)

        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("font-size: 12pt;")
        self.connect_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.connect_button)

        self.layout.addStretch()
    
    def refresh_com_ports(self):
        self.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_dropdown.addItem(port.device)
        self.com_port_dropdown.addItem("Testing")
    
    def connect(self):
        if self.radio.start(self.com_port_dropdown.currentText()):
            QMessageBox.information(self, "Status", "Connected")
        else:
            QMessageBox.information(self, "Error", "Failed to connect")