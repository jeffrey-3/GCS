class AltController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.waypoints_updated.connect(self.update_waypoints)
    
    def update_waypoints(self, waypoints):
        if len(waypoints) > 0:
            self.view.update(waypoints, waypoints[0].lat, waypoints[0].lon)
        else:
            self.view.clear()