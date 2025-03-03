from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from widgets.command_buttons import CommandButtons
from widgets.flight_display import PrimaryFlightDisplay
from widgets.map import Map
from widgets.height_profile import AltitudeGraph
from widgets.data_table import DataTable
from widgets.raw_data import RawData
from widgets.waypoint_editor import WaypointEditor
from widgets.tiles import *
from lib.data_structures.data_structures import *

class View(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()

    def init_ui(self):
        self.apply_dark_theme()
        self.setWindowTitle("UAV Ground Control")
        self.create_layouts()
        self.create_widgets()

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.map_layout, 2)
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def create_widgets(self):
        self.tabs = QTabWidget()
        self.datatable = DataTable()
        self.tabs.addTab(self.datatable, "Quick")
        self.raw_data = RawData()
        self.tabs.addTab(self.raw_data, "Raw")
        self.command_buttons = CommandButtons()
        self.tabs.addTab(self.command_buttons, "Command")

        self.pfd = PrimaryFlightDisplay()

        self.map = Map()
        self.map_layout.addWidget(self.map)
        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph)

        self.waypoint_editor = WaypointEditor()
        self.left_layout.addWidget(self.waypoint_editor)

    def start(self):
        self.left_layout.addWidget(self.pfd)
        self.waypoint_editor.setParent(None)
        self.left_layout.addWidget(self.tabs)

    def update(self, flight_data, waypoints):
        self.map.waypoints = waypoints
        
        self.raw_data.update(flight_data.queue_len)
        # Set center position to first GPS fix
        if flight_data.center_lat == 0 and flight_data.gps_fix:
            flight_data.center_lat = flight_data.lat
            flight_data.center_lon = flight_data.lon
        self.pfd.update(flight_data)
        self.datatable.update(flight_data)
        self.map.update_data(flight_data)
        self.altitude_graph.update(waypoints, flight_data)

    def load_flightplan(self, waypoints):
        self.map.waypoints = waypoints
        self.map.lat = waypoints[0].lat
        self.map.lon = waypoints[0].lon

        flight_data = FlightData()
        flight_data.center_lat = waypoints[0].lat
        flight_data.center_lon = waypoints[0].lon
        self.altitude_graph.update(waypoints, flight_data)
        self.waypoint_editor.load_flightplan(waypoints)
    
    def show_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        return file_name
    
    def alert(self, title, msg):
        QMessageBox.information(self, title, msg)

    def apply_dark_theme(self):
        self.app.setStyle("Fusion")
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
        self.app.setPalette(dark_palette)
        self.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")