from communications.input import Input
from lib.logger.logger import Logger
from communications.generate_packet import *
from lib.data_structures.data_structures import *
import json
from PyQt5.QtCore import *
from lib.utils.utils import *

class Model(QObject):
    flightplan_processed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.waypoints = []
        self.params_values = []
        self.params_format = ""
        self.input = Input()
        self.logger = Logger()
    
    def connect(self, port):
        self.input.connect(port)

    def update(self):
        flight_data = self.input.update()
        self.logger.write_log(flight_data)
        return flight_data

    def send_params(self):
        self.input.append_queue(get_params_payload(self.params_values, self.params_format))
        for i, waypoint in enumerate(self.waypoints):
            self.input.append_queue(get_wpt_payload(waypoint, i)) 
    
    def process_flightplan_file(self, path):
        f = open(path, 'r')
        json_data = json.load(f) 
        self.waypoints = [
            Waypoint(WaypointType(wp['type']), float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
            for wp in json_data
        ]    
        self.flightplan_processed.emit(self.waypoints)
    
    def process_params_file(self, path):
        file = open(path, "r")
        data = json.load(file)
        self.params_format = data['format']
        params = data['params']
        self.params_values = []
        for key in params:
            self.params_values.extend(flatten_array(params[key]))