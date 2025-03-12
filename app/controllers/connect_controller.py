from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial.tools.list_ports

class ConnectController(QObject):
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.view.refresh_button.clicked.connect(self.refresh_com_ports)
        self.view.com_port_dropdown.currentIndexChanged.connect(self.port_changed)
        self.refresh_com_ports()
        self.port_changed()

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.view.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.view.com_port_dropdown.addItem(port.device)
        self.view.com_port_dropdown.addItem("Testing")
    
    def port_changed(self):
        self.model.set_port(self.view.com_port_dropdown.currentText())