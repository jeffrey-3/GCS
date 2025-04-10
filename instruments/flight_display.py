from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from instruments.pfd import PFDView
from instruments.quick import DataView
from instruments.raw import RawView
from instruments.state import StateView
from instruments.altitude_profile import AltitudeGraph
from instruments.nav_display import NavDisplay

class FlightDisplay(QWidget):
    def __init__(self, radio, gcs):
        super().__init__()

        self.radio = radio
        self.gcs = gcs

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        self.left_layout = QVBoxLayout()
        left_container = QWidget()
        left_container.setLayout(self.left_layout)
        self.splitter.addWidget(left_container)

        self.right_layout = QGridLayout()
        right_container = QWidget()
        right_container.setLayout(self.right_layout)
        self.splitter.addWidget(right_container)

        self.add_left_widgets()
        self.add_right_widgets()
    
    def add_left_widgets(self):
        self.left_layout.addWidget(PFDView(self.radio))
        self.left_layout.addWidget(StateView())

        self.tabs = QTabWidget()
        self.tabs.setFont(self.tabs_font)
        self.tabs.addTab(DataView(), "Quick")
        self.tabs.addTab(RawView(), "Raw")
        self.left_layout.addWidget(self.tabs)

    def add_right_widgets(self):
        self.right_layout.addWidget(NavDisplay(self.radio, self.gcs), 0, 0, 1, 1)
        self.right_layout.setRowStretch(0, 3) 
        
        self.right_layout.addWidget(AltitudeGraph(self.gcs), 1, 0, 1, 1)
        self.right_layout.setRowStretch(1, 1)