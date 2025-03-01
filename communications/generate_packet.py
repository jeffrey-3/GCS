from lib.cobs import cobs
import struct

def get_cmd_payload(cmd):
    # Payload: Message ID + Command Byte
    return bytes([1]) + cmd

def get_wpt_payload(wp, wp_idx):
    # Payload: Message ID + Waypoint Index + Waypoint
    # Equals sign to remove padding
    return struct.pack("=BB3f", 2, wp_idx, wp[0], wp[1], wp[2])

def get_land_tgt_payload(lat, lon, hdg):
    # Payload: Message ID + Data
    return bytes([3]) + struct.pack("=3f", lat, lon, hdg)

def get_params_payload(values, format):
    return bytes([4]) + struct.pack(format, *values)

def get_pkt(payload):
    # Start byte, length byte, COBS byte, then payload
    return bytes([0x00]) + bytes([len(payload)]) + cobs.encode(payload)