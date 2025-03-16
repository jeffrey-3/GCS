class StateController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.data_changed.connect(self.update)
    
    def update(self, flight_data):
        self.view.update(flight_data)