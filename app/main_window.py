from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.pfd_view import PFDView
from app.views.data_view import DataView
from app.views.raw_view import RawView
from app.views.live_alt_view import LiveAltView
from app.views.tiles_view import TilesView
from app.views.map_view import MapView
from app.views.altitude_view import AltitudeGraph
from app.views.connect_view import ConnectView
from app.views.params_view import ParamsView
from app.views.plan_view import PlanView
from app.models.tiles_model import TilesModel
from app.models.plan_model import PlanModel
from app.models.telemetry_model import TelemetryModel
from app.models.params_model import ParamsModel
from app.controllers.params_controller import ParamsController
from app.controllers.connect_controller import ConnectController
from app.controllers.plan_controller import PlanController
from app.controllers.tiles_controller import TilesController
from app.controllers.raw_controller import RawController
from app.controllers.live_alt_controller import LiveAltController
from app.controllers.pfd_controller import PFDController
from app.controllers.altitude_controller import AltController
from app.controllers.map_controller import MapController
from app.controllers.data_controller import DataController
from app.utils.data_structures import *
from app.utils.utils import *

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()

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
        self.scroll_layout1 = QVBoxLayout()
        self.scroll_layout2 = QVBoxLayout()
        self.scroll_layout3 = QVBoxLayout()

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
        self.map_controller = MapController(self.map_view, self.plan_model, self.telemetry_model)
        self.right_layout.addWidget(self.map_view)

        self.altitude_graph = AltitudeGraph()
        self.alt_controller = AltController(self.altitude_graph, self.plan_model)
        self.right_layout.addWidget(self.altitude_graph)

        self.live_alt_view = LiveAltView()
        self.live_alt_controller = LiveAltController(self.live_alt_view, self.telemetry_model)
        self.live_alt_view.hide()
        self.right_layout.addWidget(self.live_alt_view, 0, 0, Qt.AlignBottom | Qt.AlignRight)
    
    def create_config_widgets(self):
        self.stacked_widget = QStackedWidget()
        self.left_layout.addWidget(self.stacked_widget)

        # Page 1: Parameters
        self.scroll_area1 = QScrollArea()
        self.scroll_area1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area1.setWidgetResizable(True)

        self.params_view = ParamsView()
        self.params_model = ParamsModel()
        self.params_controller = ParamsController(self.params_view, self.params_model)
        self.scroll_layout1.addWidget(self.params_view)

        container1 = QWidget()
        container1.setLayout(self.scroll_layout1)
        self.scroll_area1.setWidget(container1)
        self.stacked_widget.addWidget(self.scroll_area1)

        # Page 2: Flight plan
        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area2.setWidgetResizable(True)

        self.plan_view = PlanView()
        self.plan_model = PlanModel()
        self.plan_controller = PlanController(self.plan_view, self.plan_model)
        self.scroll_layout2.addWidget(self.plan_view)

        self.tiles_model = TilesModel()
        self.tiles_view = TilesView()
        self.tiles_controller = TilesController(self.tiles_view, self.tiles_model)
        self.scroll_layout2.addWidget(self.tiles_view)

        container2 = QWidget()
        container2.setLayout(self.scroll_layout2)
        self.scroll_area2.setWidget(container2)
        self.stacked_widget.addWidget(self.scroll_area2)

        # Page 3: Connect
        self.scroll_area3 = QScrollArea()
        self.scroll_area3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area3.setWidgetResizable(True)

        self.connect_view = ConnectView()
        self.telemetry_model = TelemetryModel()
        self.connect_controller = ConnectController(self.connect_view, self.telemetry_model, self.plan_model, self.params_model)
        self.scroll_layout3.addWidget(self.connect_view)

        container3 = QWidget()
        container3.setLayout(self.scroll_layout3)
        self.scroll_area3.setWidget(container3)
        self.stacked_widget.addWidget(self.scroll_area3)

        # Next button
        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.next_btn.clicked.connect(self.next_page)
        self.left_layout.addWidget(self.next_btn)

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:
            if self.params_model.get_params_values():
                self.stacked_widget.setCurrentIndex(current_index + 1)
            else:
                QMessageBox.information(self, "Error", "Parameters missing")
        elif current_index == 1:
            if self.plan_model.get_waypoints():
                self.stacked_widget.setCurrentIndex(current_index + 1)
                self.next_btn.setText("START")
            else:
                QMessageBox.information(self, "Error", "Flight plan missing")
        elif current_index == 2:
            port = self.connect_controller.get_port()
            if self.telemetry_model.connect(port):
                self.start()
            else:
                QMessageBox.information(self, "Error", "COM port incorrect")
    
    def start(self):
        # Send parameters and waypoints to vehicle
        waypoints = self.plan_model.get_waypoints()
        params_values =  self.params_model.get_params_values()
        params_format = self.params_model.get_params_format()
        self.telemetry_model.send_params(waypoints, params_values, params_format)
        
        self.stacked_widget.hide()
        self.next_btn.hide()
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