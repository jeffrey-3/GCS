import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QTextEdit
from PyQt5.QtCore import Qt

class SerialPortGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Port Connector")
        self.setGeometry(100, 100, 400, 300)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # COM Port Selection
        self.com_port_label = QLabel("Select COM Port:")
        self.layout.addWidget(self.com_port_label)

        self.com_port_dropdown = QComboBox()
        self.layout.addWidget(self.com_port_dropdown)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh COM Ports")
        self.refresh_button.clicked.connect(self.refresh_com_ports)
        self.layout.addWidget(self.refresh_button)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_serial)
        self.layout.addWidget(self.connect_button)

        # Status Display
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.layout.addWidget(self.status_display)

        # Initialize COM ports
        self.refresh_com_ports()

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_dropdown.addItem(port.device)
        if not ports:
            self.status_display.append("No COM ports found.")

    def connect_to_serial(self):
        """Connect to the selected COM port."""
        selected_port = self.com_port_dropdown.currentText()
        if selected_port:
            try:
                self.serial_connection = serial.Serial(selected_port, baudrate=9600, timeout=1)
                self.status_display.append(f"Connected to {selected_port}")
            except serial.SerialException as e:
                self.status_display.append(f"Failed to connect to {selected_port}: {e}")
        else:
            self.status_display.append("No COM port selected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialPortGUI()
    window.show()
    sys.exit(app.exec_())