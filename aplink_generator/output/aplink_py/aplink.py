
import struct

        
class aplink_nav_display:
    format = "ffB"
    msg_id = 0  
                      
    
    pos_est_north = None
    
    pos_est_east = None
    
    current_waypoint = None
    
    
    def unpack(self, bytes):
        data = struct.unpack(format, bytes)
        
        self.pos_est_north = data[0]
        
        self.pos_est_east = data[1]
        
        self.current_waypoint = data[2]
        
    
    def pack(self):
        return struct.pack(format, self.pos_est_north, self.pos_est_east, self.current_waypoint)
        
class aplink_cal_sensors:
    format = "fffffffff"
    msg_id = 1  
                      
    
    gx = None
    
    gy = None
    
    gz = None
    
    ax = None
    
    ay = None
    
    az = None
    
    mx = None
    
    my = None
    
    mz = None
    
    
    def unpack(self, bytes):
        data = struct.unpack(format, bytes)
        
        self.gx = data[0]
        
        self.gy = data[1]
        
        self.gz = data[2]
        
        self.ax = data[3]
        
        self.ay = data[4]
        
        self.az = data[5]
        
        self.mx = data[6]
        
        self.my = data[7]
        
        self.mz = data[8]
        
    
    def pack(self):
        return struct.pack(format, self.gx, self.gy, self.gz, self.ax, self.ay, self.az, self.mx, self.my, self.mz)
