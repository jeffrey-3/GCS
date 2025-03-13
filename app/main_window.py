from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.pfd_view import PFDView
from app.views.data_view import DataView
from app.views.raw_view import RawView
from app.views.live_alt_view import LiveAltView
from app.views.map_view import MapView
from app.views.start_page_view import StartPageView
from app.views.altitude_view import AltitudeGraph
from app.views.params_page_view import ParamsPageView
from app.views.plan_page_view import PlanPageView
from app.models.telemetry_model import TelemetryModel
from app.models.config_model import ConfigModel
from app.views.connect_page_view import ConnectPageView
from app.controllers.raw_controller import RawController
from app.controllers.live_alt_controller import LiveAltController
from app.controllers.pfd_controller import PFDController
from app.controllers.altitude_controller import AltController
from app.controllers.plan_page_controller import PlanPageController
from app.controllers.connect_page_controller import ConnectPageController
from app.controllers.params_page_controller import ParamsPageController
from app.controllers.map_controller import MapController
from app.controllers.data_controller import DataController
from app.utils.data_structures import *
from app.utils.utils import *

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()
        self.start_page_view.new_mission_signal.connect(self.next_page)
        self.params_page_controller.complete_signal.connect(self.next_page)
        self.plan_page_controller.complete_signal.connect(self.next_page)
        self.connect_page_controller.complete_signal.connect(self.start)

    def init_ui(self):
        self.apply_dark_theme()
        self.setWindowTitle("UAV Ground Control")
        self.create_layouts()
        self.create_config_widgets()
        self.create_data_widgets()
        self.create_map_widgets()

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QGridLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout, 2)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def create_data_widgets(self):
        """
        PFD
        """
        self.pfd_view = PFDView()
        self.pfd_controller = PFDController(self.pfd_view, self.telemetry_model)
        self.pfd_view.hide()
        self.left_layout.addWidget(self.pfd_view)

        """
        Tabs
        """
        self.tabs = QTabWidget()
        self.tabs.hide()
        self.left_layout.addWidget(self.tabs)

        self.data_view = DataView()
        self.data_controller = DataController(self.data_view, self.telemetry_model)
        self.tabs.addTab(self.data_view, "Quick")
        
        self.raw_view = RawView()
        self.raw_controller = RawController(self.raw_view, self.telemetry_model)
        self.tabs.addTab(self.raw_view, "Raw")

    def create_map_widgets(self):
        """
        Map
        """
        self.map_view = MapView()
        self.map_controller = MapController(self.map_view, self.config_model, self.telemetry_model)
        self.right_layout.addWidget(self.map_view)

        self.altitude_graph = AltitudeGraph()
        self.alt_controller = AltController(self.altitude_graph, self.config_model)
        self.right_layout.addWidget(self.altitude_graph)

        self.live_alt_view = LiveAltView()
        self.live_alt_controller = LiveAltController(self.live_alt_view, self.telemetry_model)
        self.live_alt_view.hide()
        self.right_layout.addWidget(self.live_alt_view, 0, 0, Qt.AlignBottom | Qt.AlignRight)
    
    def create_config_widgets(self):
        self.stacked_widget = QStackedWidget()
        self.left_layout.addWidget(self.stacked_widget)

        self.config_model = ConfigModel()
        self.telemetry_model = TelemetryModel()

        self.start_page_view = StartPageView()
        self.stacked_widget.addWidget(self.start_page_view)

        self.params_page_view = ParamsPageView(self.config_model)
        self.params_page_controller = ParamsPageController(self.params_page_view, self.config_model)
        self.stacked_widget.addWidget(self.params_page_view)

        self.plan_page_view = PlanPageView(self.config_model)
        self.plan_page_controller = PlanPageController(self.plan_page_view, self.config_model)
        self.stacked_widget.addWidget(self.plan_page_view)

        self.connect_page_view = ConnectPageView(self.telemetry_model)
        self.connect_page_controller = ConnectPageController(self.connect_page_view, self.telemetry_model)
        self.stacked_widget.addWidget(self.connect_page_view)
    
    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_index + 1)
    
    def start(self):
        # Send parameters and waypoints to vehicle
        waypoints = self.config_model.get_waypoints()
        params_values =  self.config_model.get_params_values()
        params_format = self.config_model.get_params_format()
        self.telemetry_model.send_params(waypoints, params_values, params_format)
        
        # Hide configuration and show flight display
        self.stacked_widget.hide()
        self.pfd_view.show()
        self.tabs.show()
        self.live_alt_view.show()

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