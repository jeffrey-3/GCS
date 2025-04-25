from comms.send_waypoints_handler import *
from comms.send_params_handler import *
from comms.serial_radio import *

# Need result signal
# Maybe each instrument has its own send waypoints handler....
# But then how do you do waypoints_updated signal?
# Maybe main creates a single object of send_waypoints_handler...

# Or in send_waypoints wait until finished signal


# How to put into testing mode for send waypoints function?

class GCS(QObject):
    cal_sensors_signal: pyqtSignal
    gps_raw_signal: pyqtSignal
    vehicle_status_full_signal: pyqtSignal
    power_signal: pyqtSignal
    rx_byte_rate_signal: pyqtSignal

    waypoints_updated = pyqtSignal(list)
    params_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.radio = SerialRadio()

        self.waypoints = List[Waypoint]
        self.params = List[Parameter]

        self.cal_sensors_signal = self.radio.cal_sensors_signal
        self.gps_raw_signal = self.radio.gps_raw_signal
        self.vehicle_status_full_signal = self.radio.vehicle_status_full_signal
        self.power_signal = self.radio.power_signal
        self.rx_byte_rate_signal = self.radio.rx_byte_rate_signal

        self.send_waypoints_handler = SendWaypointsHandler(self.radio)
        self.send_params_handler = SendParamsHandler(self.radio)

        self.send_waypoints_handler.finished_signal.connect(self._send_waypoints_finished)
    
    def start(self, port):
        return self.radio.start(port)
    
    def send_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.send_waypoints_handler.send_waypoints(waypoints) # During testing, waypoints updated doesn't get emitted

        return True

    def send_params(self, params):
        self.send_params_handler.send_params(params)
        self.params_updated.emit(params)
    
    def _send_waypoints_finished(self, success):
        if success:
            self.waypoints_updated.emit(self.waypoints)