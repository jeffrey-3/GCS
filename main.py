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
import time

app = QApplication([])
input = InputRandom()
# input = InputBluetooth()
pfd = PrimaryFlightDisplay()

class BackgroundThread(QThread):
    frame_signal = pyqtSignal(QPixmap)
    
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            input.getData()

            self.roll = input.roll
            self.pitch = input.pitch
            self.heading = input.heading
            self.altitude = input.altitude
            self.speed = input.speed 
            self.lat = input.lat 
            self.lon = input.lon

            input.send()

            self.frame_signal.emit((pfd.update(self.pitch, self.roll, self.altitude, self.speed, 80, 50)))

            time.sleep(0.00001)

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
        self.start_thread()
    
    def start_thread(self):
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
        self.map.update(self.thread.heading, self.thread.lat, self.thread.lon)

main = MainWindow()
main.showMaximized()
app.exec()