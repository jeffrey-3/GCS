from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.waypoint_editor.importButton.clicked.connect(self.open_flightplan)
        self.view.waypoint_editor.params_btn.clicked.connect(self.open_params)
        self.view.waypoint_editor.continue_btn.clicked.connect(self.start)

        self.model.flightplan_processed.connect(self.view.load_flightplan)

    def start(self):
        waypoints = self.view.waypoint_editor.getWaypoints()
        if waypoints:
            selected_port = self.view.waypoint_editor.com_port_dropdown.currentText()
            if selected_port:
                self.model.connect(selected_port)
                self.model.send_params()
                self.view.start()

                self.timer = QTimer()
                self.timer.timeout.connect(self.update)
                self.timer.start(20)
        else:
            self.view.alert("Error", "Missing waypoints or parameters")

    def update(self):
        waypoints = self.view.waypoint_editor.getWaypoints()
        flight_data = self.model.update()
        self.view.update(flight_data, waypoints)
        
    def open_flightplan(self):
        file_path = self.view.show_file_dialog()
        if file_path:
            self.model.process_flightplan_file(file_path)
    
    def open_params(self):
        file_path = self.view.show_file_dialog()
        if file_path:
            self.model.process_params_file(file_path)
            self.view.waypoint_editor.params_file_label.setText(file_path)