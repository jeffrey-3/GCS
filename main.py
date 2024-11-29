# Plan coordinates in google maps, then import or type the coordinates into GCS
# Use PyQt drawing API to draw HUD on opencv pixmap
# You can test using flightgear

import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import numpy as np
import cv2

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.plot([0, 20, 100], [0, 50, -60], pen=pg.mkPen('r', width=5))
        self.plot_graph.setXRange(-100, 100)
        self.plot_graph.setYRange(-100, 100)
        self.plot_graph.getPlotItem().hideAxis('bottom')
        self.plot_graph.getPlotItem().hideAxis('left')
        # self.plot_graph.getAxis('bottom').setTicks()
        self.plot_graph.setAspectLocked(True)
        arrow = pg.ArrowItem(angle=0, headLen=40, tipAngle=45, baseAngle=30, pen=QColor(255, 0, 0), brush=QColor(255, 0, 0))
        self.plot_graph.addItem(arrow)

        img = pg.ImageItem(cv2.cvtColor(cv2.imread("map.png"), cv2.COLOR_BGR2RGB))
        img.scale(0.5, 0.5)
        img.setZValue(-100)
        self.plot_graph.addItem(img)

app = QtWidgets.QApplication([])
main = MainWindow()
main.showFullScreen()
app.exec()