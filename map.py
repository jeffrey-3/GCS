import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import functions as fn
from flight_data import FlightData
import math
import numpy as np

class FixedOutlineRectItem(QGraphicsRectItem):
    def paint(self, painter, option, widget=None):
        # Fill the rectangle
        # painter.fillRect(self.rect(), QBrush(Qt.black))
        
        # Draw the outline with a fixed width
        # pen = QPen(Qt.white)
        # pen = pg.mkPen("white", style=Qt.DashLine)  # Outline color
        pen = pg.mkPen("white")
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
    # Geocoordinates at the center of map
    # Use runway as home?
    # Set center as first GPS packet
    center_lat = 0
    center_lon = 0

    def __init__(self):
        super().__init__()

        self.flight_data = FlightData()

        self.waypoints_numbers = []

        self.add_style()
        self.add_runway()
        self.init_waypoints()
        self.add_arrow()
        
    def add_runway(self):
        self.rwy_line = self.plot([0], [0], pen=pg.mkPen('white', width=2))
        self.rwy_marker = self.plot([0], [0], symbol="s", symbolSize=30, symbolBrush='w')
    
    def add_style(self):
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.setBackground(QColor("#202124"))

    def add_arrow(self):
        self.arrow = CenteredArrowItem(angle=90, headLen=60, tipAngle=45, baseAngle=30, pen=pg.mkPen('white', width=2), brush=QColor("black"))
        self.addItem(self.arrow)

    def init_waypoints(self):
        self.waypoints_line = self.plot([], 
                                        [], 
                                        pen=pg.mkPen('magenta', width=5), 
                                        symbol="o", 
                                        symbolSize=50, 
                                        symbolBrush=QColor("black"), 
                                        symbolPen=pg.mkPen(QColor("magenta"), width=5))
        
        # Create Target waypoint, setData later
        self.target_marker = pg.ScatterPlotItem([], [], size=100, brush=pg.mkBrush(0, 0, 0, 0), pen=pg.mkPen('white', width=2))
        self.addItem(self.target_marker)

    def update(self, flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg):
        self.flight_data = flight_data

        self.setTitle(f"<p style='white-space:pre;'>Lat:{self.flight_data.lat:.6f}      Lon:{self.flight_data.lon:.6f}</p>")

        self.waypoints = waypoints

        position = self.calculate_displacement_meters(self.flight_data.lat, self.flight_data.lon)
        self.arrow.setStyle(angle=self.flight_data.heading + 90)
        self.arrow.setPos(position[0], position[1])

        x, y = self.calculate_displacement_meters(self.waypoints[self.flight_data.wp_idx][0], self.waypoints[self.flight_data.wp_idx][1])
        self.target_marker.setData([x], [y])

        self.update_waypoints()

        rwy_e, rwy_n = self.calculate_displacement_meters(rwy_lat, rwy_lon)
        self.rwy_line.setData([rwy_e, rwy_e - 500*math.sin(math.radians(rwy_hdg))], [rwy_n, rwy_n - 500*math.cos(math.radians(rwy_hdg))])
        self.rwy_marker.setData([rwy_e], [rwy_n])
    
    def update_waypoints(self):
        x = []
        y = []
        for waypoint in self.waypoints:
            x_pt, y_pt = self.calculate_displacement_meters(waypoint[0], waypoint[1])
            x.append(x_pt)
            y.append(y_pt)
        self.waypoints_line.setData(x, y)

        # Update waypoint number labels
        for i in range(min(len(self.waypoints), len(self.waypoints_numbers))):
            self.waypoints_numbers[i].setPos(x[i], y[i])

        if len(self.waypoints_numbers) > len(self.waypoints): # WP has been removed
            for i in range(len(self.waypoints), len(self.waypoints_numbers)):
                self.removeItem(self.waypoints_numbers[i])
                self.waypoints_numbers.pop(i)
        elif len(self.waypoints) > len(self.waypoints_numbers): # WP has been added
            for i in range(len(self.waypoints_numbers), len(self.waypoints)):
                font = QFont()
                font.setPixelSize(40)
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
                text.setPos(x[i], y[i])
                text.setFont(font)
                self.addItem(text)
                self.waypoints_numbers.append(text)

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
    
    def calculate_lat_lon(self, x, y):
        # Earth's radius in meters
        R = 6378137.0

        # Convert center latitude to radians
        center_lat_rad = math.radians(self.center_lat)
        
        # Compute new latitude
        lat_rad = center_lat_rad + (y / R)
        lat = math.degrees(lat_rad)

        # Compute new longitude
        lon_rad = math.radians(self.center_lon) + (x / (R * math.cos(center_lat_rad)))
        lon = math.degrees(lon_rad)

        return lat, lon