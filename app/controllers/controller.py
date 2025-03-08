from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from app.utils.data_structures import *

"""
Controller has main loop
View has the following callbacks:
- Load flightplan file
- Load params_file
- Start
"""


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.waypoint_editor.continue_btn.clicked.connect(self.start)
        self.view.map.clicked.connect(self.view.waypoint_editor.clicked)
        self.model.flightplan_processed.connect(self.view.load_flightplan)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def start(self):
        waypoints = self.view.waypoint_editor.getWaypoints()
        if waypoints:
            selected_port = self.view.waypoint_editor.connect_view.com_port_dropdown.currentText()
            if self.model.connect(selected_port):
                self.model.send_params(waypoints)
                self.view.start()
                self.timer.start(20)
            else:
                self.view.alert("Error", "COM port incorrect")
        else:
            self.view.alert("Error", "Missing waypoints or parameters")

    def update(self):
        waypoints = self.view.waypoint_editor.getWaypoints()
        flight_data = self.model.update()
        self.view.update(flight_data, waypoints)