from app.utils.tile_downloader import TileDownloader
from app.utils.utils import *
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.utils.utils import *
import json
from dataclasses import dataclass

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float

class ConfigModel(QObject):
    waypoints_updated = pyqtSignal(list)
    map_clicked_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.params_json = ""
        self.params_values = None
        self.params_format = None
        self.waypoints = None
    
    def process_params_file(self, path):
        try:
            file = open(path, "r")
            self.params_json = json.load(file)
            
            self.params_format = "="
            self.params_values = []
            for param in self.params_json:
                self.params_format += param["type"]
                self.params_values.extend(flatten_array(param["value"]))
            
            return True  # Success
        except Exception as e:
            print(f"Error processing params file: {e}")
            return False  # Failure
    
    def get_params_values(self):
        return self.params_values

    def get_params_format(self):
        return self.params_format
    
    # Tiles
    def download(self, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, min_zoom, max_zoom):
        downloader = TileDownloader(threads=10)
        downloader.download_all_tiles((top_left_lat, top_left_lon), 
                                      (bottom_right_lat, bottom_right_lon), 
                                      min_zoom, 
                                      max_zoom)

        # QMessageBox.information(self, "Status", "Completed download")
    
    def save_file(self, waypoints, file_path):
        if waypoints:
            json_data = [
                {"lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
                for wp in waypoints
            ]
            
            if file_path:
                with open(file_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
                    return True
        return False
    
    def process_flightplan_file(self, path):
        try:
            with open(path, 'r') as f:
                json_data = json.load(f)
            
            self.waypoints = [
                Waypoint(float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
                for wp in json_data
            ]
            
            self.waypoints_updated.emit(self.waypoints)
            return True  # Success
        except Exception as e:
            print(f"Error processing flight plan file: {e}")
            return False  # Failure
    
    def update_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.waypoints_updated.emit(waypoints)
    
    def map_clicked(self, pos):
        self.map_clicked_signal.emit(pos)
    
    def get_waypoints(self):
        return self.waypoints
    
    def get_params_json(self):
        return self.params_json

    def save_last_flightplan_params(self):
        json_data = [
            {"lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
            for wp in self.waypoints
        ]

        f = open("app/resources/last_flightplan.json", "w")
        json.dump(json_data, f, indent=4)

        f = open("app/resources/last_params.json", 'w')
        json.dump(self.params_json, f, indent=4)

        print("Last flight plan and params saved")