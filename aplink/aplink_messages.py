
# Auto-generated Python

import struct
from enum import Enum
from aplink.aplink_helpers import APLink
                    

class PARAM_TYPE(Enum):
    
    INT32 = 0,
    
    FLOAT = 1,
    

class COMMAND_ID(Enum):
    
    CALIBRATE = 0,
    

class MODE_ID(Enum):
    
    CONFIG = 0,
    
    STARTUP = 1,
    
    MANUAL = 2,
    
    FBW = 3,
    
    TAKEOFF = 4,
    
    MISSION = 5,
    
    LAND = 6,
    
    FLARE = 7,
    
 

        
class aplink_vehicle_status_full:
    msg_id = 0  
                      
    
    roll = None             
    
    roll_sp = None             
    
    pitch = None             
    
    pitch_sp = None             
    
    yaw = None             
    
    alt = None             
    
    alt_sp = None             
    
    spd = None             
    
    spd_sp = None             
    
    lat = None             
    
    lon = None             
    
    current_waypoint = None             
    
    mode_id = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.roll, self.roll_sp, self.pitch, self.pitch_sp, self.yaw, self.alt, self.alt_sp, self.spd, self.spd_sp, self.lat, self.lon, self.current_waypoint, self.mode_id, = struct.unpack("=hhhhhhhhhiiBB", payload)
                    
        return True
    
    def pack(self, roll, roll_sp, pitch, pitch_sp, yaw, alt, alt_sp, spd, spd_sp, lat, lon, current_waypoint, mode_id):
        payload = struct.pack("=hhhhhhhhhiiBB", roll, roll_sp, pitch, pitch_sp, yaw, alt, alt_sp, spd, spd_sp, lat, lon, current_waypoint, mode_id)
        return APLink().pack(payload, self.msg_id)
        
class aplink_cal_sensors:
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
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.gx, self.gy, self.gz, self.ax, self.ay, self.az, self.mx, self.my, self.mz, = struct.unpack("=fffffffff", payload)
                    
        return True
    
    def pack(self, gx, gy, gz, ax, ay, az, mx, my, mz):
        payload = struct.pack("=fffffffff", gx, gy, gz, ax, ay, az, mx, my, mz)
        return APLink().pack(payload, self.msg_id)
        
class aplink_waypoint:
    msg_id = 2  
                      
    
    lat = None             
    
    lon = None             
    
    alt = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.lat, self.lon, self.alt, = struct.unpack("=iif", payload)
                    
        return True
    
    def pack(self, lat, lon, alt):
        payload = struct.pack("=iif", lat, lon, alt)
        return APLink().pack(payload, self.msg_id)
        
class aplink_gps_raw:
    msg_id = 3  
                      
    
    lat = None             
    
    lon = None             
    
    sats = None             
    
    fix = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.lat, self.lon, self.sats, self.fix, = struct.unpack("=iiB?", payload)
                    
        return True
    
    def pack(self, lat, lon, sats, fix):
        payload = struct.pack("=iiB?", lat, lon, sats, fix)
        return APLink().pack(payload, self.msg_id)
        
class aplink_hitl_sensors:
    msg_id = 4  
                      
    
    imu_ax = None             
    
    imu_ay = None             
    
    imu_az = None             
    
    imu_gx = None             
    
    imu_gy = None             
    
    imu_gz = None             
    
    mag_x = None             
    
    mag_y = None             
    
    mag_z = None             
    
    baro_asl = None             
    
    gps_lat = None             
    
    gps_lon = None             
    
    of_x = None             
    
    of_y = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.imu_ax, self.imu_ay, self.imu_az, self.imu_gx, self.imu_gy, self.imu_gz, self.mag_x, self.mag_y, self.mag_z, self.baro_asl, self.gps_lat, self.gps_lon, self.of_x, self.of_y, = struct.unpack("=ffffffffffiihh", payload)
                    
        return True
    
    def pack(self, imu_ax, imu_ay, imu_az, imu_gx, imu_gy, imu_gz, mag_x, mag_y, mag_z, baro_asl, gps_lat, gps_lon, of_x, of_y):
        payload = struct.pack("=ffffffffffiihh", imu_ax, imu_ay, imu_az, imu_gx, imu_gy, imu_gz, mag_x, mag_y, mag_z, baro_asl, gps_lat, gps_lon, of_x, of_y)
        return APLink().pack(payload, self.msg_id)
        
class aplink_hitl_commands:
    msg_id = 5  
                      
    
    rud_pwm = None             
    
    ele_pwm = None             
    
    thr_pwm = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.rud_pwm, self.ele_pwm, self.thr_pwm, = struct.unpack("=HHH", payload)
                    
        return True
    
    def pack(self, rud_pwm, ele_pwm, thr_pwm):
        payload = struct.pack("=HHH", rud_pwm, ele_pwm, thr_pwm)
        return APLink().pack(payload, self.msg_id)
        
class aplink_waypoints_count:
    msg_id = 6  
                      
    
    num_waypoints = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.num_waypoints, = struct.unpack("=B", payload)
                    
        return True
    
    def pack(self, num_waypoints):
        payload = struct.pack("=B", num_waypoints)
        return APLink().pack(payload, self.msg_id)
        
class aplink_request_waypoint:
    msg_id = 7  
                      
    
    index = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.index, = struct.unpack("=B", payload)
                    
        return True
    
    def pack(self, index):
        payload = struct.pack("=B", index)
        return APLink().pack(payload, self.msg_id)
        
class aplink_waypoints_ack:
    msg_id = 8  
                      
    
    success = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.success, = struct.unpack("=?", payload)
                    
        return True
    
    def pack(self, success):
        payload = struct.pack("=?", success)
        return APLink().pack(payload, self.msg_id)
        
class aplink_time_since_epoch:
    msg_id = 9  
                      
    
    microseconds = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.microseconds, = struct.unpack("=Q", payload)
                    
        return True
    
    def pack(self, microseconds):
        payload = struct.pack("=Q", microseconds)
        return APLink().pack(payload, self.msg_id)
        
class aplink_rc_input:
    msg_id = 10  
                      
    
    ail = None             
    
    ele = None             
    
    rud = None             
    
    thr = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.ail, self.ele, self.rud, self.thr, = struct.unpack("=bbbb", payload)
                    
        return True
    
    def pack(self, ail, ele, rud, thr):
        payload = struct.pack("=bbbb", ail, ele, rud, thr)
        return APLink().pack(payload, self.msg_id)
        
class aplink_power:
    msg_id = 11  
                      
    
    batt_volt = None             
    
    batt_curr = None             
    
    batt_used = None             
    
    ap_curr = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.batt_volt, self.batt_curr, self.batt_used, self.ap_curr, = struct.unpack("=HHHH", payload)
                    
        return True
    
    def pack(self, batt_volt, batt_curr, batt_used, ap_curr):
        payload = struct.pack("=HHHH", batt_volt, batt_curr, batt_used, ap_curr)
        return APLink().pack(payload, self.msg_id)
        
class aplink_param_set:
    msg_id = 12  
                      
    
    name = []             
    
    value = []             
    
    type = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.name, self.value, self.type, = struct.unpack("=ccccccccccccccccBBBBB", payload)
                    
        return True
    
    def pack(self, name, value, type):
        payload = struct.pack("=ccccccccccccccccBBBBB", *name, *value, type)
        return APLink().pack(payload, self.msg_id)
        
class aplink_command:
    msg_id = 13  
                      
    
    command_id = None             
    
    
    def unpack(self, payload: bytes):
        if len(payload) != struct.calcsize(self.format):
            return False
                    
        self.command_id, = struct.unpack("=B", payload)
                    
        return True
    
    def pack(self, command_id):
        payload = struct.pack("=B", command_id)
        return APLink().pack(payload, self.msg_id)
