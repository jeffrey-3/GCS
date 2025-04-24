from comms.send_waypoints_handler import *
from comms.send_params_handler import *

class GCS:
    waypoints_updated = pyqtSignal(list)
    params_updated = pyqtSignal(list)

    def __init__(self):
        self.radio = SerialRadio()
        self.send_waypoints_handler = SendWaypointsHandler(self.radio)
        self.send_params_handler = SendParamsHandler(self.radio)
    
    def send_waypoints(self, waypoints):
        self.send_waypoints_handler.send_waypoints(waypoints)

    def send_params(self, params):
        self.send_params_handler.send_params(params)