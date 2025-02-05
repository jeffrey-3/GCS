class Input():
    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.altitude = 0
        self.speed = 0
        self.lat = 0
        self.lon = 0
        self.mode_id = -1
        self.wp_idx = 0

        # When command needs to be sent, it gets added here
        # When it recieves acknowledgement, it gets removed
        self.command_queue = []
    def getData(self):
        pass
    def generate_command_packet(self, command):
        pass
    def generate_waypoint_packet(self, waypoint, waypoint_index):
        pass
    def send(self):
        pass
    def append_queue(self, packet):
        pass