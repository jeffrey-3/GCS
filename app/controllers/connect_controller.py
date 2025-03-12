from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial.tools.list_ports

class ConnectController(QObject):
    def __init__(self, view, telem_model, plan_model, params_model):
        super().__init__()

        self.view = view
        self.telem_model = telem_model
        self.plan_model = plan_model
        self.params_model = params_model

        self.view.refresh_button.clicked.connect(self.refresh_com_ports)

        self.refresh_com_ports()

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.view.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.view.com_port_dropdown.addItem(port.device)
        self.view.com_port_dropdown.addItem("Testing")
    
    def get_port(self):
        return self.view.com_port_dropdown.currentText()