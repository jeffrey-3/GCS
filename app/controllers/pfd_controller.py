class PFDController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.data_changed.connect(self.update)
    
    def update(self, data):
        self.view.update(data['latest_payload'].data.roll, 
                         data['latest_payload'].data.pitch,
                         data['latest_payload'].data.heading,
                         data['latest_payload'].data.altitude,
                         data['latest_payload'].data.airspeed)