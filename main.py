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
from logger import Logger

class MainWindow(QMainWindow):
    def __init__(self, testing):
        super().__init__()

        self.flight_data = FlightData() 
        
        if testing:
            self.input = InputRandom()
        else:
            self.input = InputBluetooth()

        self.logger = Logger()

        self.setup_window()
        self.create_layouts()
        self.create_widgets()
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
            
            self.pfd.update(self.flight_data)
            self.datatable.update(self.flight_data)
            self.command_buttons.update(len(self.input.command_queue))

            self.altitude_graph.update(waypoints, self.flight_data)
            self.map.update(self.flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg)

            self.logger.write_log(self.flight_data)
    
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
        self.waypointEditor.loadWaypoints([[33.019, -118.598, -60],
                                           [33.020, -118.596, -60]])
        self.tabs.addTab(self.waypointEditor, "Flight Plan")

        self.map = Map()
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph, 1)
            
    def start_thread(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
    
    def setup_window(self):
        self.setWindowTitle("UAV Ground Control")
    
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
        # Get default waypoints
        waypoints, rwy_lat, rwy_lon, rwy_hdg = self.waypointEditor.getWaypoints()

        # Upload waypoints through radio
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