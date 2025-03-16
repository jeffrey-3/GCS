class AltController:
    def __init__(self, view, model, telemetry_model):
        self.view = view
        self.model = model
        self.telemetry_model = telemetry_model
        self.model.waypoints_updated.connect(self.update_waypoints)
        self.telemetry_model.data_changed.connect(self.update_wp_idx)
        self.prev_wp_idx = None
    
    def update_waypoints(self, waypoints):
        if len(waypoints) > 0:
            self.view.update(waypoints, waypoints[0].lat, waypoints[0].lon, None)
        else:
            self.view.clear()
    
    # This causes lag
    def update_wp_idx(self, data):
        if not data["latest_packet"].data.target_waypoint_index == self.prev_wp_idx:
            self.prev_wp_idx = data["latest_packet"].data.target_waypoint_index
            waypoints = self.model.get_waypoints()
            self.view.update(waypoints, waypoints[0].lat, waypoints[0].lon, data["latest_packet"].data.target_waypoint_index)