class TilesController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
        self.view.download_btn.clicked.connect(self.download)
    
    def download(self):
        top_left_lat = float(self.view.top_left_lat_input.text())
        top_left_lon = float(self.view.top_left_lon_input.text())
        bottom_right_lat = float(self.view.bottom_right_lat_input.text())
        bottom_right_lon = float(self.view.bottom_right_lon_input.text())
        min_zoom = int(self.view.min_zoom_input.text())
        max_zoom = int(self.view.max_zoom_input.text())
        self.model.download(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, min_zoom, max_zoom)