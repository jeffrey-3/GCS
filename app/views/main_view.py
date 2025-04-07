from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.pfd_view import PFDView
from app.views.data_view import DataView
from app.views.raw_view import RawView
from app.views.live_alt_view import LiveAltView
from app.views.map_view import MapView
from app.views.state_view import StateView
from app.views.start_page_view import StartPageView
from app.views.reconnect_page_view import ReconnectPageView
from app.views.altitude_view import AltitudeGraph
from app.views.params_page_view import ParamsPageView
from app.views.plan_page_view import PlanPageView
from app.views.connect_page_view import ConnectPageView
from app.controllers.raw_controller import RawController
from app.controllers.live_alt_controller import LiveAltController
from app.controllers.altitude_controller import AltController
from app.controllers.state_controller import StateController
from app.controllers.plan_page_controller import PlanPageController
from app.controllers.reconnect_page_controller import ReconnectPageController
from app.controllers.connect_page_controller import ConnectPageController
from app.controllers.params_page_controller import ParamsPageController
from app.controllers.map_controller import MapController
from app.controllers.data_controller import DataController
from app.utils.utils import *

class MainView(QMainWindow):
    def __init__(self, app, radio, config_model):
        super().__init__()
        self.app = app
        self.radio = radio
        self.config_model = config_model
        self.init_ui()

    def init_ui(self):
        self.apply_dark_theme()
        self.setWindowTitle("UAV Ground Control")
        self.create_layouts()
        self.create_map_widgets()
        self.create_config_widgets()
        self.create_data_widgets()

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
        self.pfd_view = PFDView(self.radio)
        self.pfd_view.hide()
        self.left_layout.addWidget(self.pfd_view)

        self.state_view = StateView()
        self.state_controller = StateController(self.state_view, self.radio)
        self.state_view.hide()
        self.left_layout.addWidget(self.state_view)

        """
        Tabs
        """
        self.tabs = QTabWidget()
        font = QFont()
        font.setPointSize(12)
        self.tabs.setFont(font)
        self.tabs.hide()
        self.left_layout.addWidget(self.tabs)

        self.data_view = DataView()
        self.data_controller = DataController(self.data_view, self.radio)
        self.tabs.addTab(self.data_view, "Quick (1)")
        
        self.raw_view = RawView()
        self.raw_controller = RawController(self.raw_view, self.radio)
        self.tabs.addTab(self.raw_view, "Raw (2)")

    def create_map_widgets(self):
        self.map_view = MapView()
        self.map_controller = MapController(self.map_view, self.config_model, self.radio)
        self.right_layout.addWidget(self.map_view, 0, 0, 1, 2)
        self.map_view.key_press_signal.connect(self.handle_key_press)

        self.altitude_graph = AltitudeGraph()
        self.alt_controller = AltController(self.altitude_graph, self.config_model, self.radio)
        self.right_layout.addWidget(self.altitude_graph, 2, 0, 2, 1)

        self.live_alt_view = LiveAltView()
        self.live_alt_controller = LiveAltController(self.live_alt_view, self.radio)
        self.live_alt_view.hide()
        self.right_layout.addWidget(self.live_alt_view, 2, 1, 2, 1)
    
    def create_config_widgets(self):
        self.stacked_widget = QStackedWidget()
        self.left_layout.addWidget(self.stacked_widget)

        self.start_page_view = StartPageView()
        self.stacked_widget.addWidget(self.start_page_view)

        self.params_page_view = ParamsPageView(self.config_model)
        self.params_page_controller = ParamsPageController(self.params_page_view, self.config_model)
        self.stacked_widget.addWidget(self.params_page_view)

        self.plan_page_view = PlanPageView(self.config_model)
        self.plan_page_controller = PlanPageController(self.plan_page_view, self.config_model)
        self.stacked_widget.addWidget(self.plan_page_view)

        self.connect_page_view = ConnectPageView(self.radio)
        self.connect_page_controller = ConnectPageController(self.connect_page_view, self.radio)
        self.stacked_widget.addWidget(self.connect_page_view)

        self.reconnect_page_view = ReconnectPageView(self.radio)
        self.reconnect_page_controller = ReconnectPageController(self.reconnect_page_view, self.radio)
        self.stacked_widget.addWidget(self.reconnect_page_view)
    
    def keyPressEvent(self, event):
        print("Key press event in MainView")  # Debug statement
        if event.key() == 49:  # Key code for '1'
            self.tabs.setCurrentIndex(0)  # Set to Tab 1
        elif event.key() == 50:  # Key code for '2'
            self.tabs.setCurrentIndex(1)  # Set to Tab 2
        else:
            super().keyPressEvent(event)  # Pass the event to the parent class

    def handle_key_press(self, event):
        print("Key press event in MainView")  # Debug statement
        if event.key() == 49:  # Key code for '1'
            self.tabs.setCurrentIndex(0)  # Set to Tab 1
        elif event.key() == 50:  # Key code for '2'
            self.tabs.setCurrentIndex(1)  # Set to Tab 2
        else:
            super().keyPressEvent(event)  # Pass the event to the parent class

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