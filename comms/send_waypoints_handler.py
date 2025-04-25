from comms.serial_radio import *
from typing import List


# self.ser not defined

class SendWaypointsHandler(QObject):
    finished_signal = pyqtSignal(bool)

    TIMEOUT_MS = 1000

    def __init__(self, radio: SerialRadio):
        super().__init__()
        self.radio = radio
        self.waypoints: List[Waypoint] = []

        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self._handle_timeout)

        self.radio.request_waypoint_signal.connect(self._request_waypoint_handler)
        self.radio.waypoints_ack_signal.connect(self._waypoints_ack_handler)
    
    def send_waypoints(self, waypoints: List[Waypoint]):
        self.waypoints = waypoints
        self.timeout_timer.start(self.TIMEOUT_MS)

        self.radio.transmit(aplink_waypoints_count().pack(len(self.waypoints)))
    
    def _request_waypoint_handler(self, request_waypoint: aplink_request_waypoint):
        self.radio.write(aplink_waypoint().pack(
            self.waypoints[request_waypoint.index].lat * 1e7, 
            self.waypoints[request_waypoint.index].lon * 1e7, 
            self.waypoints[request_waypoint.index].alt
        ))
    
    def _waypoints_ack_handler(self, waypoints_ack: aplink_waypoints_ack):
        self.timeout_timer.stop()
        self.finished_signal.emit(waypoints_ack.success)
    
    def _handle_timeout(self):
        self.finished_signal.emit(False)