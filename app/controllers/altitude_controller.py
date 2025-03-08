class AltController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.model.waypoints_updated.connect(self.update_waypoints)
    
    def update_waypoints(self, waypoints):
        self.view.update(waypoints, waypoints[0].lat, waypoints[0].lon)