import pyqtgraph as pg
from PyQt5.QtGui import *

class AltitudeGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.plot([0, 1, 2], [0, 50, 70], pen=pg.mkPen('magenta', width=5))
        self.getAxis('left').setTextPen(pg.mkPen('white', width=3))
        self.getAxis('bottom').setTextPen(pg.mkPen('white', width=3))
        self.setMenuEnabled(False)
        self.hideButtons()