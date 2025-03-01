from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QSizePolicy, QLineEdit, QPushButton, QWidget, QFileDialog, QTabWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import json
from widgets.flight_display import PrimaryFlightDisplay
from widgets.map import Map
from widgets.height_profile import AltitudeGraph
from widgets.data_table import DataTable
from widgets.raw_data import RawData
from lib.utils.utils import flatten_array

class StartupView(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.controller = None
        self.flight_plan_dir = ""
        self.params_dir = ""
        self.init_ui()
    
    def set_controller(self, controller):
        self.controller = controller
    
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle("UAV Ground Control")
        self.setup_layout()
        self.setup_connections()
        self.apply_dark_theme()

    def setup_layout(self):
        """Set up the layout and widgets"""
        self.layout = QGridLayout()

        # Get default directories
        default_dirs_file = open("resources/last_dir.txt", "r")
        default_flightplan_dir = default_dirs_file.readline()
        default_params_dir = default_dirs_file.readline()

        # Title
        self.title_label = QLabel("<h1>UAV Ground Control<\h1>")
        self.layout.addWidget(self.title_label, 0, 0, 1, 2)

        # Flight Plan Section
        self.flight_plan_label = QLabel("Flight Plan:")
        self.flightplan_input = QLineEdit(default_flightplan_dir)
        self.flightplan_input.setFixedWidth(1000)
        self.flightplan_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.flightplan_btn = QPushButton("Search")
        self.layout.addWidget(self.flight_plan_label, 1, 0)
        self.layout.addWidget(self.flightplan_input, 1, 1)
        self.layout.addWidget(self.flightplan_btn, 1, 2)

        # Parameters section
        self.parameters_label = QLabel("Parameters:")
        self.params_input = QLineEdit(default_params_dir)
        self.params_input.setFixedWidth(1000)
        self.params_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.params_btn = QPushButton("Search")
        self.layout.addWidget(self.parameters_label, 2, 0)
        self.layout.addWidget(self.params_input, 2, 1)
        self.layout.addWidget(self.params_btn, 2, 2)

        # Continue button
        self.continue_button = QPushButton("OK")
        self.layout.addWidget(self.continue_button, 3, 0, 1, 3)

        # Set layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def setup_connections(self):
        """Connect signals to slots"""
        self.flightplan_btn.clicked.connect(lambda: self.load_file(self.flightplan_input))
        self.params_btn.clicked.connect(lambda: self.load_file(self.params_input))
        self.continue_button.clicked.connect(self.continue_process)

    def load_file(self, target_input):
        """Open a file dialog and set the selected file path to the target input"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load File", "", "All Files (*)", options=options
        )
        if file_name:
            target_input.setText(file_name)

    def continue_process(self):
        """Handle the OK button click"""
        self.flight_plan_dir = self.flightplan_input.text().strip()
        self.params_dir = self.params_input.text().strip()
        if self.flight_plan_dir and self.params_dir:
            self.save_last_directories()
            self.controller.open_main_window() 
    
    def save_last_directories(self):
        """Save the last used directories to a file"""
        f = open("resources/last_dir.txt", "w")
        f.write(f"{self.flight_plan_dir}\n{self.params_dir}")

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

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.waypoints = []
        self.init_ui()

    def init_ui(self):
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
        self.pfd = PrimaryFlightDisplay()
        self.left_layout.addWidget(self.pfd)
        self.tabs = QTabWidget()
        self.left_layout.addWidget(self.tabs)
        self.datatable = DataTable()
        self.tabs.addTab(self.datatable, "Quick")
        self.raw_data = RawData()
        self.tabs.addTab(self.raw_data, "Raw")
        self.map = Map()
        self.map_layout.addWidget(self.map, 2)
        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph, 1)

    def update(self, flight_data):
        self.raw_data.update(flight_data.queue_len)
        # Set center position to first GPS fix
        if flight_data.center_lat == 0 and flight_data.gps_fix:
            self.map.setup() # Have to setup after the entire layout setup or there will be offset from drawing (0, 0) will not be (0, 0)
            flight_data.center_lat = flight_data.lat
            flight_data.center_lon = flight_data.lon
        self.pfd.update(flight_data)
        self.datatable.update(flight_data)
        self.map.update_data(flight_data, self.waypoints, self.rwy_lat, self.rwy_lon, self.rwy_hdg)
        self.altitude_graph.update(self.waypoints, flight_data)

    def load_files(self):
        f = open("resources/last_dir.txt", "r")
        flight_plan_dir = f.readline().strip()
        params_dir = f.readline().strip()
        self.load_flight_plan(flight_plan_dir)
        self.load_params(params_dir)
        return self.params_values, self.params_format, self.rwy_lat, self.rwy_lon, self.rwy_hdg, self.waypoints
    
    def load_flight_plan(self, dir):
        f = open(dir, 'r')
        json_data = json.load(f)
        rwy_data = json_data['landing']
        self.rwy_lat = rwy_data['lat']
        self.rwy_lon = rwy_data['lon']
        self.rwy_hdg = rwy_data['hdg']
        waypoints_data = json_data['waypoints']
        for wp in waypoints_data:
            self.waypoints.append([float(wp['lat']), float(wp['lon']), float(wp['alt'])])

    def load_params(self, dir):
        file = open(dir, "r")
        data = json.load(file)
        self.params_format = data['format']
        params = data['params']
        self.params_values = []
        for key in params:
            self.params_values.extend(flatten_array(params[key]))