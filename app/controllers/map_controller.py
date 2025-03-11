class MapController:
    def __init__(self, view, model, telemetry_model):
        self.view = view
        self.model = model
        self.telemetry_model = telemetry_model

        self.telemetry_model.flight_data_updated.connect(self.update_flight_data)
        self.model.waypoints_updated.connect(self.update_waypoints)
        self.view.clicked.connect(self.map_clicked)
    
    def update_waypoints(self, waypoints):
        self.view.waypoints = waypoints
        if len(waypoints) > 0:
            self.view.lat = waypoints[0].lat
            self.view.lon = waypoints[0].lon
    
    def update_flight_data(self, flight_data):
        self.view.update_data(flight_data)
    
    def map_clicked(self, pos):
        self.model.map_clicked(pos)