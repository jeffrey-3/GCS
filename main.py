from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
from instruments.pfd import PFDView
from instruments.quick import DataView
from instruments.raw import RawView
from instruments.state import StateView
from instruments.altitude_profile import AltitudeGraph
from instruments.planner import PlanView
from instruments.params import ParamsView
from instruments.connect import ConnectView
from instruments.nav_display import NavDisplay
from utils.utils import *
from gcs import GCS
from communication.radio import Radio

# Add more signals to radio and more aplink messages
# Then you can test the other instruments like raw

# 2. Get it working with preflight sidebar removed
# 3. Test qpainter writing to QWidget instead of canvas
# 4. rename everything

# Top bar using qhboxlayout with buttons

# modern theme
# Flight view

class MainView(QMainWindow):
    def __init__(self, app, radio, gcs):
        super().__init__()
        self.app = app
        self.radio = radio
        self.gcs = gcs
        
        self.setWindowTitle("UAV Ground Control")
        self.create_layouts()
        self.create_map_widgets()
        self.create_data_widgets()

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QGridLayout()

        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 2)

        container = QWidget()
        container.setLayout(self.main_layout)

        main_tabs = QTabWidget()
        main_tabs.addTab(container, "Flight")
        main_tabs.addTab(PlanView(self.radio, self.gcs), "Waypoints")
        main_tabs.addTab(ParamsView(), "Config")
        main_tabs.addTab(ConnectView(self.radio), "Connect")
        self.setCentralWidget(main_tabs)

        font = QFont()
        font.setPointSize(12)
        main_tabs.setFont(font)

    def create_data_widgets(self):
        self.left_layout.addWidget(PFDView(self.radio))
        self.left_layout.addWidget(StateView())

        self.tabs = QTabWidget()
        self.tabs.addTab(DataView(), "Quick")
        self.tabs.addTab(RawView(), "Raw")
        self.tabs.addTab(QWidget(), "Calibrate")

        font = QFont()
        font.setPointSize(12)
        self.tabs.setFont(font)

        self.left_layout.addWidget(self.tabs)

    def create_map_widgets(self):
        self.right_layout.addWidget(NavDisplay(self.radio, self.gcs), 0, 0, 1, 1)
        self.right_layout.addWidget(AltitudeGraph(), 1, 0, 1, 1)
        self.right_layout.setRowStretch(0, 3) 
        self.right_layout.setRowStretch(1, 1)
        
if __name__ == "__main__":
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication([])

    qdarktheme.setup_theme(corner_shape="sharp")
    qdarktheme.load_palette()

    gcs = GCS()
    radio = Radio()

    main_window = MainView(app, radio, gcs)
    main_window.show()
    
    app.exec()