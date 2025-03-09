from PyQt5.QtCore import *
from communication.input import Input
from app.utils.logger import Logger
from app.utils.data_structures import *

class TelemetryModel(QObject):
    flight_data_updated = pyqtSignal(FlightData)

    def __init__(self):
        super().__init__()

        self.input = Input()
        self.logger = Logger()

        self.input.flight_data_updated.connect(self.update)

    def update(self, flight_data):
        if flight_data.center_lat == 0 and flight_data.gps_fix:
            flight_data.center_lat = flight_data.lat
            flight_data.center_lon = flight_data.lon
        self.logger.write_log(flight_data)
        self.flight_data_updated.emit(flight_data)
    
    def connect(self, port):
        return self.input.connect_and_start_thread(port)