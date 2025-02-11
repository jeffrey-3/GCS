from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph
from data_table import DataTable
from command_buttons import CommandButtons
from input_random import InputRandom
from input_bluetooth import InputBluetooth
from waypoint_editor import WaypointEditor
from logger import Logger

class MainWindow(QMainWindow):
    def __init__(self, testing):
        super().__init__()

        self.setWindowTitle("UAV Ground Control")
        
        if testing:
            self.input = InputRandom()
        else:
            self.input = InputBluetooth()

        self.logger = Logger()

        self.create_layouts()
        self.create_widgets()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

        self.showMaximized()

    def update(self):
        self.input.send()

        if self.input.getData():
            # Get flight data
            flight_data = self.input.flight_data

            self.pfd.update(flight_data)
            self.datatable.update(flight_data)
            self.command_buttons.update(len(self.input.command_queue))

            # If first GPS fix, set center
            if flight_data.center_lat == 0 and flight_data.gps_fix:
                flight_data.center_lat = flight_data.lat
                flight_data.center_lon = flight_data.lon

            self.logger.write_log(flight_data)

            # Get waypoints from user
            waypoints = self.waypointEditor.getWaypoints()

            rwy_lat = 0 
            rwy_lon = 0 
            rwy_hdg = 0
            if self.waypointEditor.get_land_target():
                rwy_lat, rwy_lon, rwy_hdg = self.waypointEditor.get_land_target()
            self.map.update(flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg)
            self.altitude_graph.update(waypoints, flight_data)
    
    def create_widgets(self):
        self.pfd = PrimaryFlightDisplay()
        self.left_layout.addWidget(self.pfd)

        self.tabs = QTabWidget()
        self.left_layout.addWidget(self.tabs)

        self.datatable = DataTable()
        self.tabs.addTab(self.datatable, "Data")

        self.command_buttons = CommandButtons()
        self.command_buttons.buttons[0].clicked.connect(self.upload_waypoints)
        self.tabs.addTab(self.command_buttons, "Commands")

        self.waypointEditor = WaypointEditor()  
        self.tabs.addTab(self.waypointEditor, "Flight Plan")

        self.map = Map()
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph, 1)
    
    def create_layouts(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout, 2)

    def upload_waypoints(self):
        # Get waypoints
        waypoints = self.waypointEditor.getWaypoints()
        rwy_lat, rwy_lon, rwy_hdg = self.waypointEditor.get_land_target()

        # Upload waypoints through radio
        for i in range(len(waypoints)):
            self.input.append_queue(self.input.generate_waypoint_packet(waypoints[i], i)) 
        
        # Upload landing target
        self.input.append_queue(self.input.generate_landing_target_packet(rwy_lat, rwy_lon, rwy_hdg))