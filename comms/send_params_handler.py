from comms.base_radio import *
from typing import List
from array import array

class SendParamsHandler(QObject):
    finished_signal = pyqtSignal(bool)

    TIMEOUT_MS = 1000

    def __init__(self, radio: BaseRadio):
        super().__init__()

        self.radio = radio
        self.param: Parameter = None

        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self._handle_timeout)

        self.radio.param_set_signal.connect(self._param_set_handler)

        self.params: List[Parameter]
        self.last_param_sent = 0

    def _param_set_handler(self, param_set: aplink_param_set):
        # TODO: Make sure param_set equal to self.param

        self.timeout_timer.stop()

        # If sent all waypoints, emit complete
        # Otherwise send next waypoint in line
        if self.last_param_sent == len(self.params) - 1:
            self.finished_signal.emit(True)
        else:
            self.last_param_sent += 1
            self._send_param(self.params[self.last_param_sent])
    
    def send_params(self, params: List[Parameter]):
        self.params = params
        self.last_param_sent = 0
        self._send_param(params[0])

    def _send_param(self, param: Parameter):        
        param_name = list(param.name.ljust(16, '\x00').encode('utf-8'))
        param_value = None
        param_type = None
        if param.type == "f":
            param_type = int(PARAM_TYPE.FLOAT)
            param_value = list(struct.pack('=f', param.value))
        elif param.type == "i":
            param_type = int(PARAM_TYPE.INT32)
            param_value = list(struct.pack('=i', param.value))
        
        print(param_name, param_value, param_type)

        self.radio.transmit(aplink_param_set().pack(param_name, param_value, param_type))
        self.timeout_timer.start(self.TIMEOUT_MS)
        self.param = param
    
    def _handle_timeout(self):
        self.finished_signal.emit(False)
        print("Params handler timeout")