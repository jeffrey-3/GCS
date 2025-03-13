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

        # Default to last flight
        self.model.process_flightplan_file("app/resources/last_flightplan.json") # It doesn't update map because map not initialized to recv signal yet...
        self.view.load_waypoints(self.model.get_waypoints())
    
    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
        if not self.model.save_file(self.view.getWaypoints(), file_path):
            QMessageBox.information(self.view, "Error", "Cannot export file. Fields missing.")
    
    def open_flightplan(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            if self.model.process_flightplan_file(file_path):
                self.view.load_waypoints(self.model.get_waypoints())
            else:
                QMessageBox.information(self.view, "Error", "File format incorrect")
    
    def waypoints_updated(self, waypoints):
        self.model.update_waypoints(waypoints)