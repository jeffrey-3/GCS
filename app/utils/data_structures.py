from dataclasses import dataclass
from enum import Enum

@dataclass
class FlightData:
    # Flight data
    roll = 0
    pitch = 0
    heading = 0
    altitude = 0
    speed = 0
    lat = 0
    lon = 0

    # Status
    mode_id = 0
    wp_idx = -1
    cell_voltage = 0
    capacity_consumed = 100
    sats = 0
    gps_fix = False
    packet_rate = 0
    current = 0
    queue_len = 0

    # Setpoints
    pitch_setpoint = 0
    heading_setpoint = 0
    alt_setpoint = 0
    speed_setpoint = 0

    # Home position
    center_lat = 0
    center_lon = 0

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float