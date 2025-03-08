from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.utils.data_structures import *
from app.utils.utils import *
import json
import datetime

class PlanModel(QObject):
    waypoints_updated = pyqtSignal(list)

    def __init__(self):
        return

    def save_file(self):
        waypoints = self.view.getWaypoints()
        if waypoints:
            json_data = [
                {"type": wp.type.value, "lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
                for wp in waypoints
            ]
            print(json_data)
            
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
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