from communications.input_bluetooth import InputBluetooth
from communications.input_random import InputRandom
from lib.logger.logger import Logger
from communications.generate_packet import *

class Model:
    def __init__(self):
        self.input = self.initialize_input()
        self.logger = Logger()

    def initialize_input(self):
        """Tries to use Bluetooth, fails back to Random Input"""
        try:
            return InputBluetooth()
        except:
            return InputRandom()
    
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