# Plan coordinates in google maps, then import or type the coordinates into GCS

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
import math
import time
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph
from datatable import DataTable

app = QApplication([])

pfd = PrimaryFlightDisplay(1000, 800)

class BackgroundThread(QThread):
    frame_signal = pyqtSignal(QPixmap)
    heading = 0

    def run(self):
        x = 0
        while True:
            roll = 5*math.cos(x/20)
            pitch = 10*math.sin(x/20)
            altitude = 50 - 30*math.sin(x/20)
            speed = 10 - 5*math.cos(x/20)
            self.heading = pitch

            self.frame_signal.emit(pfd.update(pitch, roll, altitude, speed, 80, 50))
            
            x = x + 1
            time.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.add_ui()
        self.add_plot()

        self.thread = BackgroundThread()
        self.thread.frame_signal.connect(self.update)
        self.thread.start() 
    
    def setup_window(self):
        qdarktheme.setup_theme()
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout)

    def add_ui(self):
        self.datatable = DataTable()
        self.left_layout.addWidget(self.datatable)

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
        self.map.update(self.thread.heading*2 + 90)

main = MainWindow()
main.showFullScreen()
app.exec()