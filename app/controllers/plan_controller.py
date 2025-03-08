from PyQt5.QtWidgets import *
import datetime

class PlanController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.exportButton.clicked.connect(self.save_file)
        self.view.importButton.clicked.connect(self.open_flightplan)
        self.view.table.cellChanged.connect(self.view.on_cell_changed)

        self.model.waypoints_updated.connect(self.update_waypoints)
    
    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
        self.model.save_file(self.view.getWaypoints(), file_path)
    
    def open_flightplan(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            waypoints = self.model.process_flightplan_file(file_path)
            self.update_waypoints(waypoints)

    def update_waypoints(self, waypoints):
        if waypoints:
            self.view.load_waypoints(waypoints)
            self.view.table.clearSelection()