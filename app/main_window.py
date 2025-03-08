from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.pfd_view import PrimaryFlightDisplay
from app.views.map_view import MapView
from app.views.altitude_view import AltitudeGraph
from app.views.data_view import DataTable
from app.views.raw_data import RawData
from app.views.config_view import ConfigView
from app.views.tiles_view import *
from app.views.realtime_alt_view import RealtimeAltPlot
from app.controllers.map_controller import MapController
from app.controllers.altitude_controller import AltController
from app.utils.data_structures import *

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
        self.map_layout = QGridLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.map_layout, 2)
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def create_widgets(self):
        self.tabs = QTabWidget()
        self.datatable = DataTable()
        self.raw_data = RawData()
        self.pfd = PrimaryFlightDisplay()
        self.config_view = ConfigView()
        self.map_view = MapView()
        self.map_controller = MapController(self.map_view, )
        self.altitude_graph = AltitudeGraph()
        self.realtime_alt_plot = RealtimeAltPlot()

        self.tabs.addTab(self.datatable, "Quick")
        self.tabs.addTab(self.raw_data, "Raw")
        self.map_layout.addWidget(self.map)
        self.map_layout.addWidget(self.altitude_graph)
        self.left_layout.addWidget(self.waypoint_editor)
        self.map_layout.addWidget(self.realtime_alt_plot, 0, 0, Qt.AlignBottom | Qt.AlignRight)

    def start(self):
        self.waypoint_editor.table.clearSelection()
        self.left_layout.addWidget(self.pfd)
        self.waypoint_editor.setParent(None)
        self.left_layout.addWidget(self.tabs)

    def update(self, flight_data, waypoints):
        self.raw_data.update(flight_data.queue_len)
        # Set center position to first GPS fix
        if flight_data.center_lat == 0 and flight_data.gps_fix:
            flight_data.center_lat = flight_data.lat
            flight_data.center_lon = flight_data.lon
        self.pfd.update(flight_data)
        self.datatable.update(flight_data)
        self.map.update_data(flight_data)
        self.altitude_graph.update(waypoints, flight_data.center_lat, flight_data.center_lon)
        self.realtime_alt_plot.update(flight_data.altitude, flight_data.alt_setpoint)

    def load_flightplan(self, waypoints):
        self.map.waypoints = waypoints
        self.map.lat = waypoints[0].lat
        self.map.lon = waypoints[0].lon
        self.altitude_graph.update(waypoints, waypoints[0].lat, waypoints[0].lon)
        self.waypoint_editor.load_flightplan(waypoints)
    
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