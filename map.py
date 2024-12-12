import pyqtgraph as pg
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import functions as fn

# https://stackoverflow.com/questions/49219278/pyqtgraph-move-origin-of-arrowitem-to-local-center
class CenteredArrowItem(pg.ArrowItem):
    def setStyle(self, **opts):
        # http://www.pyqtgraph.org/documentation/_modules/pyqtgraph/graphicsItems/ArrowItem.html#ArrowItem.setStyle
        self.opts.update(opts)

        opt = dict([(k,self.opts[k]) for k in ['headLen', 'tipAngle', 'baseAngle', 'tailLen', 'tailWidth']])
        tr = QTransform()
        path = fn.makeArrowPath(**opt)
        tr.rotate(self.opts['angle'])
        p = -path.boundingRect().center()
        tr.translate(p.x(), p.y())
        self.path = tr.map(path)
        self.setPath(self.path)

        self.setPen(fn.mkPen(self.opts['pen']))
        self.setBrush(fn.mkBrush(self.opts['brush']))

        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)

class Map(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.x = [0, 20, 100, 70]
        self.y = [0, 50, -60, -100]

        self.plot(self.x, self.y, pen=pg.mkPen('magenta', width=5), symbol="o", symbolSize=50, symbolBrush=QColor("magenta"), symbolPen=QColor("magenta"))
        self.setXRange(-100, 100)
        self.setYRange(-100, 100)
        self.getPlotItem().hideAxis('bottom')
        self.getPlotItem().hideAxis('left')
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.setBackground(QColor("#006500"))

        # Add numbers
        font = QFont()
        font.setPixelSize(40)
        for i in range(len(self.x)):
            text = None 
            if i == 1: # Show the current waypoint being tracked
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5)) # pg.TextItem(text=str(i), color=QColor("white"), fill=QColor("magenta"), anchor=(0.5, 0.5))
            else:
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
            text.setPos(self.x[i], self.y[i])
            text.setFont(font)
            self.addItem(text)

        # Add arrow to plot
        self.arrow = CenteredArrowItem(angle=90, headLen=60, tipAngle=45, baseAngle=30, pen=pg.mkPen('black', width=3), brush=QColor("red"))
        self.addItem(self.arrow)

        # Add image to plot
        img = pg.ImageItem(cv2.cvtColor(cv2.imread("map.png"), cv2.COLOR_BGR2RGB))
        img.setZValue(-100)
        self.addItem(img)

        tr = QTransform()
        tr.scale(2, 2)
        tr.translate(-img.width()/2, -img.height()/2)
        img.setTransform(tr)

    def update(self, heading, x, y):
        self.arrow.setStyle(angle=heading)
        self.arrow.setPos(x, y)