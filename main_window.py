from PyQt5.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from modules.pfd import PrimaryFlightDisplay
from map import Map
from modules.altitude_graph import AltitudeGraph
from modules.data_table import DataTable
from input_random import InputRandom
from input_bluetooth import InputBluetooth
from logger import Logger
import json

class MainWindow(QMainWindow):
    # Add default to example
    def __init__(self, testing, flight_plan_dir, params_dir):
        super().__init__()

        self.flight_plan_dir = flight_plan_dir
        self.params_dir = params_dir

        self.waypoints = []

        self.setWindowTitle("UAV Ground Control")

        self.showMaximized()

        self.load_file()

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

    def update(self):
        self.input.send()

        if self.input.getData():
            # Get flight data
            flight_data = self.input.flight_data

            self.pfd.update(flight_data)
            self.datatable.update(flight_data)

            # If first GPS fix, set center
            if flight_data.center_lat == 0 and flight_data.gps_fix:
                flight_data.center_lat = flight_data.lat
                flight_data.center_lon = flight_data.lon

            self.logger.write_log(flight_data)

            self.map.update(flight_data, self.waypoints, self.rwy_lat, self.rwy_lon, self.rwy_hdg)
            self.altitude_graph.update(self.waypoints, flight_data)
    
    def create_widgets(self):
        self.pfd = PrimaryFlightDisplay()
        self.left_layout.addWidget(self.pfd)

        self.tabs = QTabWidget()
        self.left_layout.addWidget(self.tabs)

        self.datatable = DataTable()
        self.tabs.addTab(self.datatable, "Quick")

        # Raw data, queue len, etc.
        self.tabs.addTab(QWidget(), "Other")

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
        # Upload waypoints through radio
        for i in range(len(self.waypoints)):
            self.input.append_queue(self.input.generate_waypoint_packet(self.waypoints[i], i)) 
        
        # Upload landing target
        self.input.append_queue(self.input.generate_landing_target_packet(self.rwy_lat, self.rwy_lon, self.rwy_hdg))
    
    def load_file(self):
        f = open(self.flight_plan_dir, 'r')
        json_data = json.load(f)

        print("Imported File:", json.dumps(json_data, indent=2))

        rwy_data = json_data['landing']

        self.rwy_lat = rwy_data['lat']
        self.rwy_lon = rwy_data['lon']
        self.rwy_hdg = rwy_data['hdg']

        waypoints_data = json_data['waypoints']

        for wp in waypoints_data:
            self.waypoints.append([float(wp['lat']), float(wp['lon']), float(wp['alt'])])