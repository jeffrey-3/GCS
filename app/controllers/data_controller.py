class DataController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.data_changed.connect(self.update)
    
    def update(self, data):
        self.view.update(data["latest_payload"].data.gps_fix, 
                         data["latest_payload"].data.gps_sats,
                         data["byte_rate"],
                         data["latest_payload"].data.cell_voltage,
                         data["latest_payload"].data.battery_current,
                         data["latest_payload"].data.capacity_consumed)