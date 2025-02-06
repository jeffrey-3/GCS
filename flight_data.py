from dataclasses import dataclass

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
    mode_id = 2
    wp_idx = 0

    # Setpoints
    pitch_setpoint = 0
    heading_setpoint = 0
    alt_setpoint = 0
    speed_setpoint = 0