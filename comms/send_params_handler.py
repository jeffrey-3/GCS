from comms.serial_radio import *
from typing import List
from array import array

class SendParamsHandler(QObject):
    finished_signal = pyqtSignal(bool)

    TIMEOUT_MS = 1000

    def __init__(self, radio: SerialRadio):
        super().__init__()

        self.radio = radio
        self.param: Parameter = None

        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self._handle_timeout)

        self.radio.param_set_signal.connect(self._param_set_handler)

    def _param_set_handler(self, param_set: aplink_param_set):
        self.timeout_timer.stop()
        self.finished_signal.emit(True)

    def send_param(self, param: Parameter):
        self.param = param

        param_name = param.name.ljust(16, '\x00')[16:].encode('utf-8') # Convert to 16-byte char array
        param_value = None
        param_type = None
        if param.name == "f":
            param_type = PARAM_TYPE.FLOAT
            param_value = array.array('B', struct.pack('=f', param.value))
        elif param.name == "i":
            param_type = PARAM_TYPE.INT32
            param_value = array.array('B', struct.pack('=i', param.value))
            
        self.ser.write(aplink_param_set().pack(param_name, param_value, param_type))
    
    def _handle_timeout(self):
        self.finished_signal.emit(False)