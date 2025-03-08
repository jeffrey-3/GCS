from communication.input import Input
from app.utils.logger import Logger
from communication.generate_packet import *
from app.utils.data_structures import *
import json
from PyQt5.QtCore import *
from app.utils.utils import *

class Model(QObject):
    def __init__(self):
        super().__init__()
        self.params_values = []
        self.params_format = ""
        self.input = Input()
        self.logger = Logger()
    
    def connect(self, port):
        return self.input.connect(port)

    def update(self):
        flight_data = self.input.update()
        self.logger.write_log(flight_data)
        return flight_data

    def send_params(self, waypoints):
        self.input.append_queue(get_params_payload(self.params_values, self.params_format))
        for i, waypoint in enumerate(waypoints):
            self.input.append_queue(get_wpt_payload(waypoint, i)) 