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
    def __init__(self, radio):
        super().__init__()

        self.radio = radio

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

        self.splitter.setStretchFactor(0, 1) 
        self.splitter.setStretchFactor(1, 2) 

        self.add_left_widgets()
        self.add_right_widgets()
    
    def add_left_widgets(self):
        self.vsplitter = QSplitter(Qt.Vertical)
        self.left_layout.addWidget(self.vsplitter)

        self.vsplitter.addWidget(PFDView(self.radio))

        self.left_sub_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.left_sub_layout)
        self.vsplitter.addWidget(container)

        self.left_sub_layout.addWidget(StateView())

        self.tabs = QTabWidget()
        self.tabs.setFont(self.tabs_font)
        self.tabs.addTab(DataView(), "Quick")
        self.tabs.addTab(RawView(), "Raw")
        self.left_sub_layout.addWidget(self.tabs)

        self.vsplitter.setStretchFactor(0, 1) 
        self.vsplitter.setStretchFactor(1, 2)

    def add_right_widgets(self):
        self.right_layout.addWidget(NavDisplay(self.radio), 0, 0, 1, 1)
        self.right_layout.setRowStretch(0, 3) 
        
        self.right_layout.addWidget(AltitudeGraph(self.radio), 1, 0, 1, 1)
        self.right_layout.setRowStretch(1, 1)