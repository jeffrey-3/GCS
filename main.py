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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.add_hud()
        self.add_ui()
        self.create_plot()
    
    def add_hud(self):
        label = QLabel()
        pixmap = QPixmap("640x480.png")
        label.setPixmap(pixmap)
        # label.resize(pixmap.width(), pixmap.height())
        self.left_layout.addWidget(label, alignment=Qt.AlignCenter)
    
    def add_ui(self):
        label = QLabel("Voltage")
        label.adjustSize()
        self.voltage_bar = QProgressBar(self)
        self.voltage_bar.setValue(30)
        self.left_layout.addWidget(self.voltage_bar)

        self.current_bar = QProgressBar(self)
        self.current_bar.setValue(30)
        self.left_layout.addWidget(self.current_bar)

    def setup_window(self):
        # Apply style to window
        # self.setStyleSheet("background-color: grey;") 
        return

    def create_main_layout(self):
        # Create layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Add layout to window
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
    
    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        # Add layout to window
        self.main_layout.addLayout(self.left_layout)

    def create_plot(self):
        # Create plot
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.plot([0, 20, 100], [0, 50, -60], pen=pg.mkPen('y', width=5))
        self.plot_graph.setXRange(-100, 100)
        self.plot_graph.setYRange(-100, 100)
        self.plot_graph.getPlotItem().hideAxis('bottom')
        self.plot_graph.getPlotItem().hideAxis('left')
        self.plot_graph.setAspectLocked(True)

        # Add arrow to plot
        self.arrow = pg.ArrowItem(angle=0, headLen=40, tipAngle=45, baseAngle=30, pen=QColor(255, 0, 0), brush=QColor(255, 0, 0))
        self.plot_graph.addItem(self.arrow)

        # Add image to plot
        img = pg.ImageItem(cv2.cvtColor(cv2.imread("map.png"), cv2.COLOR_BGR2RGB))
        img.scale(0.5, 0.5)
        img.setZValue(-100)
        self.plot_graph.addItem(img)

        # Add plot to layout
        self.main_layout.addWidget(self.plot_graph)

app = QApplication([])
main = MainWindow()
main.showFullScreen()
app.exec()