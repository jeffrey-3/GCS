from utils.utils import *
from instruments.map import MapView

class NavDisplay(MapView):
    def __init__(self, radio, gcs):
        super().__init__(gcs)
        self.radio = radio
        self.gcs = gcs
        self.waypoints = self.gcs.get_waypoints()

        if self.waypoints is not None:
            self.map_lat = self.waypoints[0].lat
            self.map_lon = self.waypoints[0].lon
        self.radio.nav_display_signal.connect(self.nav_display_update)
    
    def nav_display_update(self, north, east, waypoint_index):
        self.waypoints = self.gcs.get_waypoints()

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