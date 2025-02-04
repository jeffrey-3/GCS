from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph
from datatable import DataTable
from command_buttons import CommandButtons
from input_random import InputRandom
from input_bluetooth import InputBluetooth
import numpy as np
from waypoint_editor import WaypointEditor
import csv
import time

csvfile = open('log.csv', 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',')

# Bug: Doesn't work when USB used. You have to load waypoints first.
# The slow loading of waypoints is due to the delay
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.waypointEditor = WaypointEditor()   
        self.pfd = PrimaryFlightDisplay()
        # self.input = InputRandom()
        self.input = InputBluetooth()

        # Lat, lon, down
        self.waypoints = [[33.0214, -118.5981, -40],
                          [33.0214, -118.6024, -40],
                          [33.0196, -118.6024, -40],
                          [33.0196, -118.5981, -40],
                          [33.0223, -118.5970, -40]]
        self.waypointEditor.setDefaultWaypoints(self.waypoints)

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.add_datatable()
        self.add_plot()
        self.start_thread()
    
    def start_thread(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
    
    def setup_window(self):
        self.setWindowTitle("UAV Ground Control")
        qdarktheme.setup_theme()
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout, 2)

    def add_datatable(self):
        self.tabs = QTabWidget()
        self.datatable = DataTable()
        self.command_buttons = CommandButtons()
        self.command_buttons.wp_button.clicked.connect(self.upload_waypoints)
        self.tabs.addTab(self.datatable, "Data")
        self.tabs.addTab(self.command_buttons, "Commands")
        self.tabs.addTab(self.waypointEditor, "Mission")
        self.tabs.addTab(QWidget(), "Raw Data")
        self.left_layout.addWidget(self.tabs)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_hud(self):
        self.hud_label = QLabel()
        self.hud_label.setPixmap(self.pfd.update(0, 0, 0, 0, 0, 0, 0))
        self.left_layout.addWidget(self.hud_label)

    def add_plot(self):
        self.map = Map(self.waypoints)
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph(self.waypoints)
        self.map_layout.addWidget(self.altitude_graph)
    
    def upload_waypoints(self):
        for i in range(len(self.waypoints)):
            self.input.append_queue(self.input.generate_waypoint_packet(self.waypoints[i], i)) 
    
    def update(self):
        self.input.send()
        
        if self.input.getData():
            # Update GUI
            self.hud_label.setPixmap(self.pfd.update(self.input.pitch, 
                                                     self.input.roll, 
                                                     self.input.heading, 
                                                     self.input.altitude, 
                                                     self.input.speed, 
                                                     0, 
                                                     0))
            self.waypoints = self.waypointEditor.getWaypoints()
            self.altitude_graph.update(self.waypoints)
            self.map.update(self.input.heading, 
                            self.input.lat, 
                            self.input.lon, 
                            self.input.wp_idx,
                            self.waypoints)
            self.datatable.update(self.input.mode_id)
            self.command_buttons.update(len(self.input.command_queue))

            csvwriter.writerow([time.time(),
                                self.input.roll, 
                                self.input.pitch, 
                                self.input.heading, 
                                self.input.altitude, 
                                self.input.speed,
                                self.input.lat,
                                self.input.lon,
                                self.input.mode_id,
                                self.input.wp_idx])

if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.showMaximized()
    app.exec()