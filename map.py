import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import functions as fn
import math
import numpy as np

# https://stackoverflow.com/questions/49219278/pyqtgraph-move-origin-of-arrowitem-to-local-center
class CenteredArrowItem(pg.ArrowItem):
    def setStyle(self, **opts):
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
    def __init__(self, waypoints):
        super().__init__()

        self.waypoints = waypoints

        # Geocoordinates at the center of map tile
        self.center_lat = 33.017826
        self.center_lon = -118.602432

        custom_pen = QPen(QColor("#FFFFFF"))
        # custom_pen.setWidth(3)
        custom_pen.setDashPattern([10, 5])
        self.dashed_line = self.plot([0, 300], [0, 300], pen=custom_pen)

        self.plot(self.waypoints[:, 1], self.waypoints[:, 0], pen=pg.mkPen('magenta', width=5), symbol="o", symbolSize=50, symbolBrush=QColor("black"), symbolPen=pg.mkPen(QColor("magenta"), width=5))
        # self.getPlotItem().hideAxis('bottom')
        # self.getPlotItem().hideAxis('left')
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.setBackground(QColor("#202124"))

        self.setRange(xRange=(-1000, 1000), yRange=(-1000, 1000))

        # Add numbers
        font = QFont()
        font.setPixelSize(40)
        for i in range(self.waypoints.shape[0]):
            text = None 
            if i == 1: # Show the current waypoint being tracked
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5)) # pg.TextItem(text=str(i), color=QColor("white"), fill=QColor("magenta"), anchor=(0.5, 0.5))
            else:
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
            text.setPos(self.waypoints[i, 1], self.waypoints[i, 0])
            text.setFont(font)
            self.addItem(text)

        # Add arrow to plot
        self.arrow = CenteredArrowItem(angle=90, headLen=60, tipAngle=45, baseAngle=30, pen=pg.mkPen('white', width=2), brush=QColor("black"))
        self.addItem(self.arrow)

    def update(self, heading, lat, lon):
        position = self.calculate_displacement_meters(lat, lon)
        self.arrow.setStyle(angle=heading + 90)
        self.arrow.setPos(position[0], position[1])

        # Heading line
        length = 0
        # length = math.sqrt((self.viewRange()[0][1] - self.viewRange()[0][0])**2 + (self.viewRange()[1][1] - self.viewRange()[1][0])**2)
        self.dashed_line.setData([position[0], position[0] + length*math.sin(math.radians(heading))], 
                                 [position[1], position[1] + length*math.cos(math.radians(heading))])
    
    def calculate_displacement_meters(self, lat, lon):
        # Earth's radius in meters
        R = 6378137.0
        
        # Convert degrees to radians
        center_lat_rad = math.radians(self.center_lat)
        center_lon_rad = math.radians(self.center_lon)
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Differences in coordinates
        delta_lat = lat_rad - center_lat_rad
        delta_lon = lon_rad - center_lon_rad
        
        # Approximate Cartesian coordinates
        x = R * delta_lon * math.cos((center_lat_rad + lat_rad) / 2)
        y = R * delta_lat
        
        return x, y