class MapController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.model.waypoints_updated.connect(self.update_waypoints)
    
    def update_waypoints(self, waypoints):
        self.view.waypoints = waypoints
        self.view.lat = waypoints[0].lat
        self.view.lon = waypoints[0].lon