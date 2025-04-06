from aplink import APLink
import struct

class CalSensors:
    MSG_ID = 15
    STRUCT_FORMAT = '=9f'  # 9 floats (no padding)

    ax = 0
    ay = 0
    az = 0
    gx = 0
    gy = 0
    gz = 0
    mx = 0
    my = 0
    mz = 0
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.STRUCT_FORMAT):
            return False
        
        data = struct.unpack(self.STRUCT_FORMAT, payload)
        self.ax = float(data[0])
        self.ay = float(data[1])
        self.az = float(data[2])
        self.gx = float(data[3])
        self.gy = float(data[4])
        self.gz = float(data[5])
        self.mx = float(data[6])
        self.my = float(data[7])
        self.mz = float(data[8])

        return True
    
    def pack(self, ax, ay, az, gx, gy, gz, mx, my, mz):
        payload = struct.pack(self.STRUCT_FORMAT, ax, ay, az, gx, gy, gz, mx, my, mz)
        return APLink().pack(payload, self.MSG_ID)