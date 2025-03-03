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
        self.flightplan_loaded = False
        self.input = Input()
        self.logger = Logger()
    
    def connect(self, port):
        self.input.connect(port)

    def update(self):
        flight_data = self.input.update()
        self.logger.write_log(flight_data)
        return flight_data

    def send_params(self, params_values, params_format, rwy_lat, rwy_lon, rwy_hdg, waypoints):
        """Upload parameters and waypoints"""
        self.input.append_queue(get_params_payload(params_values, params_format))
        for i, waypoint in enumerate(waypoints):
            self.input.append_queue(get_wpt_payload(waypoint, i)) 
        self.input.append_queue(get_land_tgt_payload(rwy_lat, rwy_lon, rwy_hdg))
    
    def process_flightplan_file(self, path):
        f = open(path, 'r')
        json_data = json.load(f) 
        self.waypoints = [
            Waypoint(WaypointType(wp['type']), float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
            for wp in json_data
        ]     
        self.flightplan_loaded = True
        self.flightplan_processed.emit(self.waypoints)
    
    def process_params_file(self, path):
        if self.flightplan_loaded:
            file = open(path, "r")
            data = json.load(file)
            params_format = data['format']
            params = data['params']
            params_values = []
            for key in params:
                params_values.extend(flatten_array(params[key]))

            self.send_params(params_values, params_format, self.rwy_lat, self.rwy_lon, self.rwy_hdg, self.waypoints)
        else:
            print("Flight plan not loaded!")