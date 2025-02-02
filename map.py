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

        # Use runway as center?
        # Geocoordinates at the center of map
        self.center_lat = 33.017826
        self.center_lon = -118.602432

        self.add_style()
        self.add_waypoints()
        self.add_arrow()
        self.add_runway()
        
    def add_runway(self):
        return
    
    def add_style(self):
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.setBackground(QColor("#202124"))

    def add_arrow(self):
        self.arrow = CenteredArrowItem(angle=90, headLen=60, tipAngle=45, baseAngle=30, pen=pg.mkPen('white', width=2), brush=QColor("black"))
        self.addItem(self.arrow)

    def add_waypoints(self):
        self.plot(self.waypoints[:, 1], 
                  self.waypoints[:, 0], 
                  pen=pg.mkPen('magenta', width=5), 
                  symbol="o", 
                  symbolSize=50, 
                  symbolBrush=QColor("black"), 
                  symbolPen=pg.mkPen(QColor("magenta"), width=5))
    
        # Waypoint Numbers
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

    def update(self, heading, lat, lon):
        position = self.calculate_displacement_meters(lat, lon)
        self.arrow.setStyle(angle=heading + 90)
        self.arrow.setPos(position[0], position[1])
    
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
    