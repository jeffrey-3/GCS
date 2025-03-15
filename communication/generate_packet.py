from lib.cobs import cobs
import struct

TELEM_MSG_ID = 0
WPT_MSG_ID = 1
PARAMS_MSG_ID = 2

def get_wpt_payload(wp, wp_idx, num_waypoints):
    # Payload: Message ID + Waypoint Index + Waypoint
    # Equals sign to remove padding
    return struct.pack("=BBB3f", WPT_MSG_ID, wp_idx, num_waypoints, wp.lat, wp.lon, wp.alt)

def get_params_payload(values, format):
    return bytes([PARAMS_MSG_ID]) + struct.pack(format, *values)

def get_pkt(payload):
    # Start byte, length byte, COBS byte, then payload
    return bytes([0x00]) + bytes([len(payload)]) + cobs.encode(payload)

def get_payload(packet):
    return