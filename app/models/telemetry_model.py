from PyQt5.QtCore import *
from communication.radio import Radio
from app.utils.logger import Logger
from communication.generate_packet import *

class TelemetryModel(QObject):
    data_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.radio = Radio()
        self.logger = Logger()
        self.port = ""
        self.radio.tlm_recv.connect(self.telemetry_recv)
    
    def set_port(self, port):
        self.port = port

    def connect(self):
        return self.radio.start(self.port)

    def telemetry_recv(self, data):
        self.logger.write_log(data["latest_packet"])
        self.data_changed.emit(data)
    
    def send_params(self, waypoints, params_values, params_format):
        self.radio.append_queue(get_params_payload(params_values, params_format))
        for i, waypoint in enumerate(waypoints):
            self.radio.append_queue(get_wpt_payload(waypoint, i, len(waypoints))) 
    
    def get_data(self):
        self.radio.get_data()