from PyQt5.QtWidgets import *
import datetime

class PlanController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.exportButton.clicked.connect(self.save_file)
        self.view.importButton.clicked.connect(self.open_flightplan)
        self.view.updated_waypoints.connect(self.waypoints_updated)
        self.model.map_clicked_signal.connect(self.view.clicked)
    
    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
        self.model.save_file(self.view.getWaypoints(), file_path)
    
    def open_flightplan(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            waypoints = self.model.process_flightplan_file(file_path)
            if waypoints:
                self.view.load_waypoints(waypoints)
                self.view.table.clearSelection()
    
    def waypoints_updated(self, waypoints):
        print("Plan Controller: Waypoints Updated")
        self.model.update_waypoints(waypoints)