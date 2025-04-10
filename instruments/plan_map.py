from instruments.map import MapView

class PlanMap(MapView):
    def __init__(self, radio, gcs):
        super().__init__(gcs)
        self.waypoints = gcs.get_waypoints() 

        if self.waypoints is not None:
            self.map_lat = self.waypoints[0].lat
            self.map_lon = self.waypoints[0].lon

        self.gcs.waypoints_updated.connect(self.set_waypoints)
    
    def set_waypoints(self, waypoints):
        self.waypoints = waypoints
        if self.map_lat == 0:  # If the map is not yet centered
            self.pan_to_home()