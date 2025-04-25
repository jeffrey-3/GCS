from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from instruments.pfd import PFDView
from instruments.quick import DataView
from instruments.raw import RawView
from instruments.state import StateView
from instruments.altitude_profile import AltitudeGraph
from utils.utils import *
from instruments.map import MapView
from aplink.aplink_messages import *
from gcs import *
from typing import List
from instruments.planner import Waypoint

class FlightDisplay(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()

        self.gcs = gcs
        self.gcs.waypoints_updated.connect(self.waypoints_updated)
        self.gcs.vehicle_status_full_signal.connect(self.vehicle_status_full_update)

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        left_container = QWidget()
        left_container.setLayout(self.left_layout)
        self.splitter.addWidget(left_container)

        self.right_layout = QGridLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        right_container = QWidget()
        right_container.setLayout(self.right_layout)
        self.splitter.addWidget(right_container)

        self.add_left_widgets()
        self.add_right_widgets()
    
    def vehicle_status_full_update(self, vehicle_status: aplink_vehicle_status_full):
        if vehicle_status.current_waypoint != self.alt_graph.current_waypoint_index:
            self.alt_graph.set_current_waypoint_index(vehicle_status.current_waypoint)
        
        self.map.set_plane_coords(vehicle_status.lat, vehicle_status.lon)
        self.map.map_lat = vehicle_status.lat
        self.map.map_lon = vehicle_status.lon
        self.map.plane_hdg = vehicle_status.yaw
        self.map.plane_current_wp = vehicle_status.current_waypoint
        
        self.map.render()

    def waypoints_updated(self, waypoints: List[Waypoint]):
        self.alt_graph.set_waypoints(waypoints)
        self.map.set_waypoints(waypoints)
        self.map.render()
    
    def add_left_widgets(self):
        self.vsplitter = QSplitter(Qt.Vertical)
        self.left_layout.addWidget(self.vsplitter)

        self.vsplitter.addWidget(PFDView(self.gcs))

        self.left_sub_layout = QVBoxLayout()
        self.left_sub_layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setLayout(self.left_sub_layout)
        self.vsplitter.addWidget(container)

        self.left_sub_layout.addWidget(StateView(self.gcs))

        self.tabs = QTabWidget()
        self.tabs.setFont(self.tabs_font)
        self.tabs.addTab(DataView(self.gcs), "Quick")
        self.tabs.addTab(RawView(self.gcs), "Raw")
        self.left_sub_layout.addWidget(self.tabs)

        self.vsplitter.setStretchFactor(0, 1) 
        self.vsplitter.setStretchFactor(1, 1)
        # self.vsplitter.setHandleWidth(0)  # Hide the resize handle

    def add_right_widgets(self):
        self.map = MapView()
        self.right_layout.addWidget(self.map, 0, 0, 1, 1)
        self.right_layout.setRowStretch(0, 3) 
        
        self.alt_graph = AltitudeGraph()
        self.right_layout.addWidget(self.alt_graph, 1, 0, 1, 1)
        self.right_layout.setRowStretch(1, 1)