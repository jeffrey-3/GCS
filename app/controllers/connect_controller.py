from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial.tools.list_ports

class ConnectController(QObject):
    start_signal = pyqtSignal()

    def __init__(self, view, model, plan_model, params_model):
        super().__init__()

        self.view = view
        self.model = model
        self.plan_model = plan_model
        self.params_model = params_model

        self.waypoints = None

        self.view.refresh_button.clicked.connect(self.refresh_com_ports)
        self.view.continue_btn.clicked.connect(self.connect)

        self.plan_model.waypoints_updated.connect(self.update_waypoints)

        self.refresh_com_ports()

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.view.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.view.com_port_dropdown.addItem(port.device)
        self.view.com_port_dropdown.addItem("Testing")
    
    def connect(self):
        if self.waypoints and self.params_model.params_values:
            port = self.view.com_port_dropdown.currentText()
            if self.model.connect(port):
                self.model.send_params(self.waypoints, self.params_model.params_values, self.params_model.params_format)
                self.start_signal.emit()
            else:
                QMessageBox.information(self.view, "Error", "COM port incorrect")
        else:
            QMessageBox.information(self.view, "Error", "Waypoints or parameters missing")

    def update_waypoints(self, waypoints):
        self.waypoints = waypoints