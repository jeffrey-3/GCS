class StateController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.model.data_changed.connect(self.update)
    
    def update(self, data):
        self.view.update(data["latest_payload"].data.mode_id)