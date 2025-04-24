from comms.serial_radio import *

class SendWaypointsHandler:
    finished_signal = pyqtSignal(bool)

    def __init__(self, radio: SerialRadio):
        self.radio = radio
        self.waypoints: List[Waypoint] = []
        self.radio.request_waypoint_signal.connect(self.request_waypoint_handler)
        self.radio.waypoints_ack_signal.connect(self.waypoints_ack_handler)
    
    def send_waypoints(self, waypoints: List[Waypoint]):
        self.waypoints = waypoints
        self.ser.write(aplink_waypoints_count().pack(len(self.waypoints)))
    
    def request_waypoint_handler(self, request_waypoint: aplink_request_waypoint):
        self.ser.write(aplink_waypoint().pack(
            self.waypoints[request_waypoint.index].lat * 1e7, 
            self.waypoints[request_waypoint.index].lon * 1e7, 
            self.waypoints[request_waypoint.index].alt
        ))
    
    def waypoints_ack_handler(self, waypoints_ack: aplink_waypoints_ack):
        self.finished_signal.emit(waypoints_ack.success)