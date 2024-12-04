import pyqtgraph as pg
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Map(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.plot([0, 20, 100], [0, 50, -60], pen=pg.mkPen('magenta', width=5))
        self.setXRange(-100, 100)
        self.setYRange(-100, 100)
        self.getPlotItem().hideAxis('bottom')
        self.getPlotItem().hideAxis('left')
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()

        # Add arrow to plot
        self.arrow = pg.ArrowItem(angle=90, headLen=40, tipAngle=45, baseAngle=30, pen=QColor("red"), brush=QColor("red"))
        self.addItem(self.arrow)

        # Add image to plot
        img = pg.ImageItem(cv2.cvtColor(cv2.imread("map.png"), cv2.COLOR_BGR2RGB))
        img.setZValue(-100)
        self.addItem(img)

        tr = QTransform()
        tr.translate(-img.width()/2, -img.height()/2)
        img.setTransform(tr)