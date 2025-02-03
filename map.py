import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import functions as fn
import math
import numpy as np

class FixedOutlineRectItem(QGraphicsRectItem):
    def paint(self, painter, option, widget=None):
        # Fill the rectangle
        # painter.fillRect(self.rect(), QBrush(Qt.black))
        
        # Draw the outline with a fixed width
        # pen = QPen(Qt.white)
        pen = pg.mkPen("white", style=Qt.DashLine)  # Outline color
        pen.setWidthF(2)  # Fixed outline width in pixels
        pen.setCosmetic(True)  # Ensures the width stays constant
        painter.setPen(pen)
        painter.drawRect(self.rect())

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

        # Geocoordinates at the center of map
        # Use runway as home?
        # Set center as first GPS packet
        self.center_lat = 33.017
        self.center_lon = -118.602

        self.rwy_lat = 33.017826
        self.rwy_lon = -118.602432
        self.rwy_len = 100
        self.rwy_width = 10
        self.rwy_hdg = 70
        self.landing_dist = 500

        self.add_style()
        self.add_runway()
        self.add_waypoints()
        self.add_arrow()
        
    def add_runway(self):
        rwy_e, rwy_n = self.calculate_displacement_meters(self.rwy_lat, self.rwy_lon)

        self.plot([rwy_e - self.rwy_len*0.5*math.sin(math.radians(self.rwy_hdg)), rwy_e - self.landing_dist*math.sin(math.radians(self.rwy_hdg))], 
                  [rwy_n - self.rwy_len*0.5*math.cos(math.radians(self.rwy_hdg)), rwy_n - self.landing_dist*math.cos(math.radians(self.rwy_hdg))], 
                  pen=pg.mkPen("white", width=2, style=Qt.DashLine))

        rwy = FixedOutlineRectItem(0, 0, self.rwy_width, self.rwy_len)
        transform = QTransform()
        transform.rotate(-self.rwy_hdg)
        transform.translate(-self.rwy_width/2, -self.rwy_len/2)
        rwy.setTransform(transform)
        self.addItem(rwy)

        rwy.setPos(rwy_e, rwy_n)

        # Create final approach WP
        # Don't need to create waypoint, but landing guidance uses waypoint at landing point and virtual approach WP at same heading, distance away
    
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
        
        # Target waypoint
        self.target_marker = pg.ScatterPlotItem([self.waypoints[0, 1]], [self.waypoints[0, 0]], size=100, brush=pg.mkBrush(0, 0, 0, 0), pen=pg.mkPen('white', width=2))
        self.addItem(self.target_marker)
    
        # Waypoint Numbers
        font = QFont()
        font.setPixelSize(40)
        for i in range(self.waypoints.shape[0]):
            text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
            text.setPos(self.waypoints[i, 1], self.waypoints[i, 0])
            text.setFont(font)
            self.addItem(text)

    def update(self, heading, lat, lon, wp_idx):
        position = self.calculate_displacement_meters(lat, lon)
        self.arrow.setStyle(angle=heading + 90)
        self.arrow.setPos(position[0], position[1])
        self.target_marker.setData([self.waypoints[wp_idx, 1]], [self.waypoints[wp_idx, 0]])
    
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
    