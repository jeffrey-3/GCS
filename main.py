# Import picture of map with geo coordinates of center
# Calculate position of the plane's geocoordinates relative to the geocoordinates of the center of map
# Put marker at the calculated displacement in meters
# Map tile downloaders:
# https://github.com/AliFlux/MapTilesDownloader
# https://www.cartograph.eu/v3/online-map-tile-downloader/


# Plan coordinates in google maps, then import or type the coordinates into GCS

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
import time
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph
from datatable import DataTable
from command_buttons import CommandButtons
from input import Input

app = QApplication([])
input = Input("socket")
pfd = PrimaryFlightDisplay(1000, 800)

class BackgroundThread(QThread):
    # Class variables
    frame_signal = pyqtSignal(QPixmap)
    heading = 0
    
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            roll, pitch, altitude, speed = input.getData()
            self.heading = pitch

            self.frame_signal.emit(pfd.update(pitch, roll, altitude, speed, 80, 50))
            
            time.sleep(1/15)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.add_datatable()
        self.add_plot()

        self.thread = BackgroundThread()
        self.thread.frame_signal.connect(self.update)
        self.thread.start() 
    
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
        self.tabs.addTab(self.datatable, "Data")
        self.tabs.addTab(self.command_buttons, "Commands")
        self.tabs.addTab(QWidget(), "Terminal") # Raw telemetry packets
        self.left_layout.addWidget(self.tabs)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_hud(self):
        self.hud_label = QLabel()
        self.left_layout.addWidget(self.hud_label)

    def add_plot(self):
        self.map = Map()
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph()
        self.map_layout.addWidget(self.altitude_graph)
    
    @pyqtSlot(QPixmap)
    def update(self, pixmap):
        self.hud_label.setPixmap(pixmap)
        self.map.update(self.thread.heading*2 + 90, 0, self.thread.heading*2)

main = MainWindow()
main.showMaximized()
app.exec()