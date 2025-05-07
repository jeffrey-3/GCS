from comms.send_waypoints_handler import *
from comms.send_params_handler import *
from comms.base_radio import *
from comms.testing_radio import *
from comms.serial_radio import *

class GCS(QObject):
    cal_sensors_signal = pyqtSignal(aplink_cal_sensors)
    gps_raw_signal = pyqtSignal(aplink_gps_raw)
    vehicle_status_full_signal = pyqtSignal(aplink_vehicle_status_full)
    power_signal = pyqtSignal(aplink_power)
    rx_byte_rate_signal = pyqtSignal(int)

    waypoints_updated = pyqtSignal(list)
    params_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.waypoints = List[Waypoint]
        self.params = List[Parameter]
    
    def start(self, port):
        radio: BaseRadio = None
        if port == "Testing":
            radio = TestingRadio()
        else:
            radio = SerialRadio()
        
        radio.cal_sensors_signal.connect(self.cal_sensors_signal)
        radio.gps_raw_signal.connect(self.gps_raw_signal)
        radio.vehicle_status_full_signal.connect(self.vehicle_status_full_signal)
        radio.power_signal.connect(self.power_signal)
        radio.rx_byte_rate_signal.connect(self.rx_byte_rate_signal)

        self.send_waypoints_handler = SendWaypointsHandler(radio)
        self.send_params_handler = SendParamsHandler(radio)
        self.send_waypoints_handler.finished_signal.connect(self._send_waypoints_finished)
        self.send_params_handler.finished_signal.connect(self._send_params_finished)

        return radio.start(port)
    
    def send_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.send_waypoints_handler.send_waypoints(waypoints)

    def send_params(self, params: List[Parameter]):
        self.params = params
        self.send_params_handler.send_params(params)
    
    def _send_waypoints_finished(self, success):
        if success:
            self.waypoints_updated.emit(self.waypoints)
    
    def _send_params_finished(self, success):
        if success:
            self.params_updated.emit(self.params)
        else:
            print("error sending params (i need a way to display this in ui, this message is just temporary)")
            # Maybe if it times out just keep sending over again