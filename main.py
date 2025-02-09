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
from flight_data import FlightData
from landmark import Landmark
import datetime
import csv
import time

class MainWindow(QMainWindow):
    def __init__(self, testing):
        super().__init__()

        self.flight_data = FlightData() 
        
        if testing:
            self.input = InputRandom()
        else:
            self.input = InputBluetooth()

        self.waypointEditor = WaypointEditor()  
        self.waypointEditor.loadWaypoints([[33.019, -118.598, -60],
                                           [33.020, -118.596, -60]])

        self.setup_filewriter()
        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_pfd()
        self.add_datatable()
        self.add_plot()
        self.start_thread()
        self.showMaximized()

    def update(self):
        self.input.send()

        if self.input.getData():
            # Get flight data
            self.flight_data = self.input.flight_data

            # Get waypoints from user
            waypoints, rwy_lat, rwy_lon, rwy_hdg = self.waypointEditor.getWaypoints()

            # If first GPS fix, set center
            if self.flight_data.center_lat == 0 and self.flight_data.gps_fix:
                self.flight_data.center_lat = self.flight_data.lat
                self.flight_data.center_lon = self.flight_data.lon
            
            self.hud_label.setPixmap(self.pfd.update(self.flight_data))
            self.datatable.update(self.flight_data)
            self.command_buttons.update(len(self.input.command_queue))

            self.altitude_graph.update(waypoints, self.flight_data)
            self.map.update(self.flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg)

            self.write_log()
    
    def write_log(self):
        self.csvwriter.writerow([time.time(),
                                 self.flight_data.roll, 
                                 self.flight_data.pitch, 
                                 self.flight_data.heading, 
                                 self.flight_data.altitude, 
                                 self.flight_data.speed,
                                 self.flight_data.lat,
                                 self.flight_data.lon,
                                 self.flight_data.mode_id,
                                 self.flight_data.wp_idx])
            
    def start_thread(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
    
    def setup_filewriter(self):
        self.csvfile = open('Logs/{date:%Y_%m_%d_%H_%M_%S}.csv'.format(date=datetime.datetime.now()), 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile, delimiter=',')
    
    def setup_window(self):
        self.setWindowTitle("UAV Ground Control")
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout, 2)

    def add_datatable(self):
        self.tabs = QTabWidget()
        self.datatable = DataTable()
        self.command_buttons = CommandButtons()
        self.command_buttons.buttons[0].clicked.connect(self.upload_waypoints)
        self.tabs.addTab(self.datatable, "Data")
        self.tabs.addTab(self.command_buttons, "Commands")
        self.tabs.addTab(self.waypointEditor, "Flight Plan")
        self.left_layout.addWidget(self.tabs)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_pfd(self):
        # Init PFD
        self.pfd = PrimaryFlightDisplay()

        # Add PFD to layout
        self.hud_label = QLabel()
        self.hud_label.setPixmap(self.pfd.update(self.flight_data))
        self.left_layout.addWidget(self.hud_label)

    def add_plot(self):
        landmarks = [Landmark(lat=33.017815, lon=-118.602486, name="Runway Begin"),
                     Landmark(lat=33.02, lon=-118.6, name="Test Landmark 2"),]
        self.map = Map(landmarks)
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph, 1)
    
    def upload_waypoints(self):
        # Get default waypoints
        waypoints, rwy_lat, rwy_lon, rwy_hdg = self.waypointEditor.getWaypoints()

        # Upload waypoints
        for i in range(len(waypoints)):
            self.input.append_queue(self.input.generate_waypoint_packet(waypoints[i], i)) 
        
        # Upload landing target
        self.input.append_queue(self.input.generate_landing_target_packet(rwy_lat, rwy_lon, rwy_hdg))

def apply_dark_theme(app):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

if __name__ == "__main__":
    app = QApplication([])
    apply_dark_theme(app)

    main = MainWindow(True)

    app.exec()