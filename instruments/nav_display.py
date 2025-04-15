from utils.utils import *
from instruments.map import MapView

class NavDisplay(MapView):
    def __init__(self, radio):
        super().__init__(radio)
        self.radio = radio
        self.waypoints = []

        if len(self.waypoints) > 0:
            self.map_lat = self.waypoints[0].lat
            self.map_lon = self.waypoints[0].lon
        self.radio.nav_display_signal.connect(self.nav_display_update)
        self.radio.waypoints_updated.connect(self.update_waypoints)
    
    def nav_display_update(self, north, east, waypoint_index):
        self.waypoints = self.radio.get_waypoints()

        if len(self.waypoints) == 0:
            return

        self.plane_lat, self.plane_lon = calculate_new_coordinate(
            self.waypoints[0].lat,
            self.waypoints[0].lon,
            north,
            east
        )
        self.map_lat, self.map_lon = calculate_new_coordinate(
            self.waypoints[0].lat,
            self.waypoints[0].lon,
            north,
            east
        )
        self.plane_current_wp = waypoint_index
        
        self.render()
    
    def update_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.map_lat = self.waypoints[0].lat # well not really needed because I will never upload waypoints without vehicle connected
        self.map_lon = self.waypoints[0].lon # Actually maybe needed because I can upload waypoints before GPS fix and before position estimate
        self.render()