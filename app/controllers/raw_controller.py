class RawController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.model.data_changed.connect(self.update)
    
    def update(self, data):
        self.view.update(data["latest_payload"].data.roll,
                         data["latest_payload"].data.pitch, 
                         data["latest_payload"].data.heading, 
                         data["latest_payload"].data.gnss_latitude, 
                         data["latest_payload"].data.gnss_longitude, 
                         data["queue_length"], 
                         data["latest_payload"].data.altitude,
                         data["latest_payload"].data.airspeed,
                         data["latest_payload"].data.position_estimate_north,
                         data["latest_payload"].data.position_estimate_east)