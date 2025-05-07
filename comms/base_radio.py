from PyQt5.QtCore import *
from aplink.aplink_messages import *
from dataclasses import dataclass
from abc import ABC, ABCMeta, abstractmethod

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float

@dataclass
class Parameter:
    name: str
    value: float
    type: str

class QABCMeta(type(QObject), ABCMeta):
    pass

class BaseRadio(QObject, ABC, metaclass=QABCMeta):
    cal_sensors_signal = pyqtSignal(aplink_cal_sensors)
    gps_raw_signal = pyqtSignal(aplink_gps_raw)
    vehicle_status_full_signal = pyqtSignal(aplink_vehicle_status_full)
    power_signal = pyqtSignal(aplink_power)
    request_waypoint_signal = pyqtSignal(aplink_request_waypoint)
    waypoints_ack_signal = pyqtSignal(aplink_waypoints_ack)
    param_set_signal = pyqtSignal(aplink_param_set)
    rx_byte_rate_signal = pyqtSignal(int)

    @abstractmethod
    def start(self, port) -> bool:
        pass

    @abstractmethod
    def transmit(self, bytes):
        pass