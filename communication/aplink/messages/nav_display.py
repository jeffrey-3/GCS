from communication.aplink.aplink import APLink
import struct

class NavDisplay:
    MSG_ID = 15
    STRUCT_FORMAT = '=3f'

    pos_est_north = 0
    pos_est_east = 0
    waypoint_index = 0
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.STRUCT_FORMAT):
            return False
        
        data = struct.unpack(self.STRUCT_FORMAT, payload)
        self.pos_est_north = float(data[0])
        self.pos_est_east = float(data[1])
        self.waypoint_index = int(data[2])

        return True
    
    def pack(self, ax, ay, az, gx, gy, gz, mx, my, mz):
        payload = struct.pack(self.STRUCT_FORMAT, ax, ay, az, gx, gy, gz, mx, my, mz)
        return APLink().pack(payload, self.MSG_ID)