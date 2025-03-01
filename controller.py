from PyQt5.QtCore import QTimer

class Controller:
    def __init__(self, model, startup_view, main_view):
        self.model = model
        self.startup_view = startup_view
        self.main_view = main_view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
    
    def open_main_window(self):
        """Closes startup window and opens the main GCS window"""
        self.startup_view.close()
        params_values, params_format, rwy_lat, rwy_lon, rwy_hdg, waypoints = self.main_view.load_files()
        self.model.send_params(params_values, params_format, rwy_lat, rwy_lon, rwy_hdg, waypoints)
        self.main_view.showMaximized()
        self.timer.start(20)

    def update(self):
        flight_data = self.model.update()
        self.main_view.update(flight_data)