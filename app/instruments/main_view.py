from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.instruments.pfd_view import PFDView
from app.instruments.data_view import DataView
from app.instruments.raw_view import RawView
from app.instruments.live_alt_view import LiveAltView
from app.instruments.map_view import MapView
from app.instruments.state_view import StateView
from app.instruments.altitude_view import AltitudeGraph
from app.instruments.plan_view import PlanView
from app.instruments.params_view import ParamsView
from app.instruments.connect_view import ConnectView
from app.utils.utils import *

class MainView(QMainWindow):
    def __init__(self, app, radio, gcs):
        super().__init__()
        self.app = app
        self.radio = radio
        self.gcs = gcs
        
        self.apply_dark_theme()
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
        self.setCentralWidget(container)

    def create_data_widgets(self):
        self.left_layout.addWidget(PFDView(self.radio))
        self.left_layout.addWidget(StateView())

        self.tabs = QTabWidget()
        self.tabs.addTab(DataView(), "Quick")
        self.tabs.addTab(RawView(), "Raw")
        self.tabs.addTab(ParamsView(), "Parameters")
        self.tabs.addTab(PlanView(), "Waypoints")
        self.tabs.addTab(QWidget(), "Calibrate")
        self.tabs.addTab(ConnectView(self.radio), "Connect")
        self.tabs.addTab(QWidget(), "HITL")

        font = QFont()
        font.setPointSize(12)
        self.tabs.setFont(font)

        self.left_layout.addWidget(self.tabs)

    def create_map_widgets(self):
        self.right_layout.addWidget(MapView(self.radio, self.gcs), 0, 0, 1, 1)
        self.right_layout.addWidget(AltitudeGraph(), 1, 0, 1, 1)
        # self.right_layout.addWidget(LiveAltView(), 1, 1, 1, 1)

        # Set stretch factors - first row (map) gets more space, second row less
        self.right_layout.setRowStretch(0, 3)  # Map gets 3 parts
        self.right_layout.setRowStretch(1, 1)   # Graphs get 1 part each
    
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