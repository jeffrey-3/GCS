# Plan coordinates in google maps, then import or type the coordinates into GCS
# Use PyQt drawing API to draw HUD on opencv pixmap
# You can test using flightgear

import pyqtgraph as pg
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2
import qdarktheme
import math
import time
from pfd import PrimaryFlightDisplay

app = QApplication([])
qdarktheme.setup_theme()

pfd = PrimaryFlightDisplay(1000, 800)

class MyThread(QThread):
    frame_signal = pyqtSignal(QPixmap)

    def run(self):
        x = 0
        while True:
            roll = 5*math.cos(x/50)
            print(roll)

            self.frame_signal.emit(pfd.update(30*math.sin(x/50), roll))
            
            x = x + 1
            time.sleep(0.01)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.create_ui_layout()
        
        self.add_ui()
        self.add_plot()
    
    def setup_window(self):
        # Apply style to window
        # self.setStyleSheet("background-color: black") 
        return
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout)

    def create_ui_layout(self):
        self.ui_layout = QGridLayout()
        self.left_layout.addLayout(self.ui_layout)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_hud(self):
        self.hud_label = QLabel()
        self.left_layout.addWidget(self.hud_label)

        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)
        self.camera_thread.start()  

    @pyqtSlot(QPixmap)
    def setImage(self,image):
        self.hud_label.setPixmap(image)   
    
    def add_ui(self):
        self.state_label = QLabel("State<h1>123087</h1>")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.state_label, 0, 0)

        self.rssi_label = QLabel("RSSI<h1>123087</h1>")
        self.rssi_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.rssi_label, 0, 1,)

        self.voltage_label = QLabel("Voltage (V)<h1>123087</h1>")
        self.voltage_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.voltage_label, 1, 0)

        self.current_label = QLabel("Current (A)<h1>123087</h1>")
        self.current_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.current_label, 1, 1)

        self.flight_time_label = QLabel("Time<h1>123087</h1>")
        self.flight_time_label.setAlignment(Qt.AlignCenter)
        self.ui_layout.addWidget(self.flight_time_label, 2, 0, 1, 2)

    def add_plot(self):
        # Create plot
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.plot([0, 20, 100], [0, 50, -60], pen=pg.mkPen('y', width=5))
        self.plot_graph.setXRange(-100, 100)
        self.plot_graph.setYRange(-100, 100)
        self.plot_graph.getPlotItem().hideAxis('bottom')
        self.plot_graph.getPlotItem().hideAxis('left')
        self.plot_graph.setAspectLocked(True)
        self.plot_graph.setMenuEnabled(False)
        self.plot_graph.hideButtons()

        # Add arrow to plot
        self.arrow = pg.ArrowItem(angle=0, headLen=40, tipAngle=45, baseAngle=30, pen=QColor(255, 0, 0), brush=QColor(255, 0, 0))
        self.plot_graph.addItem(self.arrow)

        # Add image to plot
        img = pg.ImageItem(cv2.cvtColor(cv2.imread("map.png"), cv2.COLOR_BGR2RGB))
        img.setZValue(-100)
        self.plot_graph.addItem(img)

        tr = QTransform()
        tr.translate(-img.width()/2, -img.height()/2)
        img.setTransform(tr)

        # Add plot to layout
        self.map_layout.addWidget(self.plot_graph, 2)

        # line graph
        self.altitude_graph = pg.PlotWidget()
        self.altitude_graph.plot([0, 1, 2], [0, 50, 70], pen=pg.mkPen('y', width=5))
        self.altitude_graph.setMenuEnabled(False)
        self.altitude_graph.hideButtons()

        self.map_layout.addWidget(self.altitude_graph)

main = MainWindow()
main.showFullScreen()
app.exec()