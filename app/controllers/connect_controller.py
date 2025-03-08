import serial.tools.list_ports

class ConnectController:
    def __init__(self, view):
        self.view = view

        self.view.refresh_button.clicked.connect(self.refresh_com_ports)

        self.refresh_com_ports()

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.view.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.view.com_port_dropdown.addItem(port.device)
        self.view.com_port_dropdown.addItem("Testing")