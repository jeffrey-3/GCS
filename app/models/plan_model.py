from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.utils.data_structures import *
from app.utils.utils import *
import json
import datetime

class PlanModel(QObject):
    waypoints_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def save_file(self, waypoints, file_path):
        if waypoints:
            json_data = [
                {"type": wp.type.value, "lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
                for wp in waypoints
            ]
            print(json_data)
            
            if file_path:
                with open(file_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
        else:
            QMessageBox.information(self, "Error", "Cannot export file. Fields missing.")
    
    def process_flightplan_file(self, path):
        f = open(path, 'r')
        json_data = json.load(f) 
        waypoints = [
            Waypoint(WaypointType(wp['type']), float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
            for wp in json_data
        ]    
        self.waypoints_updated.emit(waypoints)