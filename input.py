from flight_data import FlightData

class Input():
    def __init__(self):
        self.flight_data = FlightData()

        # When command needs to be sent, it gets added here
        # When it recieves acknowledgement, it gets removed
        self.command_queue = []
    def getData(self):
        pass
    def generate_command_packet(self, command):
        pass
    def generate_waypoint_packet(self, waypoint, waypoint_index):
        pass
    def generate_landing_target_packet(self, lat, lon, hdg):
        pass
    def send(self):
        pass
    def append_queue(self, packet):
        pass