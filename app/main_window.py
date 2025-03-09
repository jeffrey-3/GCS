from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.pfd_view import PFDView
from app.views.data_view import DataView
from app.views.raw_view import RawView
from app.views.live_alt_view import RealtimeAltPlot
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
from app.controllers.connect_controller import ConnectController
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
        self.connect_controller.start_signal.connect(self.start)

    def init_ui(self):
        self.apply_dark_theme()
        self.setWindowTitle("UAV Ground Control")
        self.create_layouts()
        self.create_widgets()

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QGridLayout()
        self.scroll_layout = QVBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout, 2)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def create_widgets(self):
        """
        Config
        """
        self.scroll_area = QScrollArea()
        
        self.tiles_model = TilesModel()
        self.tiles_view = TilesView()
        self.tiles_controller = TilesController(self.tiles_view, self.tiles_model)
        self.scroll_layout.addWidget(self.tiles_view)

        self.params_view = ParamsView()
        self.params_model = ParamsModel()
        self.params_controller = ParamsController(self.params_view, self.params_model)
        self.scroll_layout.addWidget(self.params_view)

        self.plan_view = PlanView()
        self.plan_model = PlanModel()
        self.plan_controller = PlanController(self.plan_view, self.plan_model)
        self.scroll_layout.addWidget(self.plan_view)

        self.connect_view = ConnectView()
        self.telemetry_model = TelemetryModel()
        self.connect_controller = ConnectController(self.connect_view, self.telemetry_model, self.plan_model, self.params_model)
        self.scroll_layout.addWidget(self.connect_view)

        container = QWidget()
        container.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(container)
        self.scroll_area.setMinimumWidth(container.width() + 50)
        self.left_layout.addWidget(self.scroll_area)

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

        """
        Map
        """
        self.map_view = MapView()
        self.map_controller = MapController(self.map_view, self.plan_model, self.telemetry_model)
        self.right_layout.addWidget(self.map_view)

        self.altitude_graph = AltitudeGraph()
        self.alt_controller = AltController(self.altitude_graph, self.plan_model)
        self.right_layout.addWidget(self.altitude_graph)

        self.live_alt_view = RealtimeAltPlot()
        self.live_alt_controller = LiveAltController(self.live_alt_view, self.telemetry_model)
        self.live_alt_view.hide()
        self.right_layout.addWidget(self.live_alt_view, 0, 0, Qt.AlignBottom | Qt.AlignRight)
    
    def start(self):
        self.scroll_area.hide()
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