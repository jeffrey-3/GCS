from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.utils.data_structures import *
from app.utils.utils import *
import json
import datetime

class PlanModel(QObject):
    waypoints_updated = pyqtSignal(list)
    map_clicked_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        self.waypoints = None

    def save_file(self, waypoints, file_path):
        if waypoints:
            json_data = [
                {"type": wp.type.value, "lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
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
                Waypoint(WaypointType(wp['type']), float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
                for wp in json_data
            ]
            
            self.waypoints_updated.emit(self.waypoints)
            return True  # Success
        except Exception as e:
            print(f"Error processing flight plan file: {e}")
            return False  # Failure
    
    def update_waypoints(self, waypoints):
        self.waypoints_updated.emit(waypoints)
    
    def map_clicked(self, pos):
        self.map_clicked_signal.emit(pos)
    
    def get_waypoints(self):
        return self.waypoints