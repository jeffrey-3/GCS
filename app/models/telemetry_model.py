from PyQt5.QtCore import *
from communication.input import Input
from app.utils.logger import Logger
from app.utils.data_structures import *
from communication.generate_packet import *

class TelemetryModel(QObject):
    flight_data_updated = pyqtSignal(FlightData)

    def __init__(self):
        super().__init__()
        self.input = Input()
        self.logger = Logger()
        self.port = ""
        self.input.flight_data_updated.connect(self.update)
    
    def set_port(self, port):
        self.port = port

    def connect(self):
        return self.input.connect_and_start_thread(self.port)

    def update(self, flight_data):
        self.logger.write_log(flight_data)
        self.flight_data_updated.emit(flight_data)
    
    def send_params(self, waypoints, params_values, params_format):
        self.input.append_queue(get_params_payload(params_values, params_format))
        for i, waypoint in enumerate(waypoints):
            self.input.append_queue(get_wpt_payload(waypoint, i, len(waypoints))) 