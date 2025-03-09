class LiveAltController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.flight_data_updated.connect(self.update)
    
    def update(self, flight_data):
        self.view.update(flight_data.altitude, flight_data.alt_setpoint)