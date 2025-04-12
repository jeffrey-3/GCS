from communication.aplink.aplink import APLink
import struct

class VFRHUD:
    MSG_ID = 15
    STRUCT_FORMAT = '=4hH3hH4B'

    roll = 0
    pitch = 0
    yaw = 0
    alt = 0
    spd = 0
    roll_sp = 0
    pitch_sp = 0
    alt_sp = 0
    spd_sp = 0
    system_mode = 0
    flight_mode = 0
    manual_mode = 0
    auto_mode = 0
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.STRUCT_FORMAT):
            return False
        
        data = struct.unpack(self.STRUCT_FORMAT, payload)
        self.roll = float(data[0]) / 100
        self.pitch = float(data[1]) / 100
        self.yaw = float(data[2]) / 100
        self.alt = float(data[3]) / 10
        self.spd = float(data[4])
        self.roll_sp = float(data[5]) / 100
        self.pitch_sp = float(data[6]) / 100
        self.alt_sp = float(data[7]) / 10
        self.spd_sp = float(data[8])
        self.system_mode = int(data[9])
        self.flight_mode = int(data[10])
        self.manual_mode = int(data[11])
        self.auto_mode = int(data[12])

        return True
    
    def pack(self, roll, pitch, yaw, alt, spd, roll_sp, pitch_sp, alt_sp, spd_sp, system_mode, flight_mode, manual_mode, auto_mode):
        payload = struct.pack(self.STRUCT_FORMAT, roll, pitch, yaw, alt, spd, roll_sp, pitch_sp, alt_sp, spd_sp, system_mode, flight_mode, manual_mode, auto_mode)
        return APLink().pack(payload, self.MSG_ID)