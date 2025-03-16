class RawController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.model.data_changed.connect(self.update)
    
    def update(self, data):
        self.view.update(data["latest_packet"].data.roll,
                         data["latest_packet"].data.pitch, 
                         data["latest_packet"].data.heading, 
                         data["latest_packet"].data.gnss_latitude, 
                         data["latest_packet"].data.gnss_longitude, 
                         data["queue_length"], 
                         data["latest_packet"].data.altitude,
                         data["latest_packet"].data.airspeed)