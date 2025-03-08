from PyQt5.QtWidgets import *

class PlanController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.exportButton.clicked.connect(self.save_file)
        self.view.importButton.clicked.connect(self.open_flightplan)

        self.model.updated_waypoints.connect(self.update_waypoints)
    
    def save_file(self):
        self.model.save_file()
    
    def open_flightplan(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            waypoints = self.model.process_flightplan_file(file_path)
            self.changed_waypoints(waypoints)

    def update_waypoints(self, waypoints):
        self.view.load_waypoints(waypoints)
        self.view.table.clearSelection()