from comms.serial_radio import *

class SendParamsHandler:
    finished_signal = pyqtSignal(bool)

    def __init__(self, radio: SerialRadio):
        self.radio = radio
        self.params: List[Parameter] = []
        self.radio.param_set_signal.connect(self.param_set_handler)
    
    def send_params(self, params: List[Parameter]):
        self.params = params
        self.send_param(self.params)

    def param_set_handler(self, param_set: aplink_param_set):
        return

    def send_param(self, param: Parameter):
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