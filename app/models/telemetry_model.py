from PyQt5.QtCore import *
from communication.radio import Radio
from app.utils.logger import Logger
from communication.binary_struct import *

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
        self.logger.write_log(data["latest_payload"])
        self.data_changed.emit(data)
    
    def send_params(self, waypoints, params_values, params_format):
        # self.radio.append_queue(get_params_payload(params_values, params_format))

        for i, waypoint in enumerate(waypoints):
            payload = WaypointPayload()
            payload.set_data(waypoint_index = i, num_waypoints = len(waypoints), lat = waypoint.lat, lon = waypoint.lon, alt = waypoint.alt)
            self.radio.add_payload_to_queue(payload) 
    
    def get_data(self):
        self.radio.get_data()