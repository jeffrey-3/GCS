import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import functions as fn
from utils import calculate_displacement_meters
import math

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
    def __init__(self):
        super().__init__()

        self.set_style()
        self.init_runway()
        self.init_waypoints()
        self.add_arrow()

    def set_style(self):
        self.setAspectLocked(True)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.setBackground(QColor("#202124")) 

    def init_runway(self):
        self.rwy_line = self.plot([0], [0], pen=pg.mkPen('white', width=2))
        self.rwy_marker = self.plot([0], [0], symbol="s", symbolSize=30, symbolBrush='w')

    def add_arrow(self):
        self.arrow = CenteredArrowItem(angle=90, headLen=60, tipAngle=45, baseAngle=30, pen=pg.mkPen('white', width=2), brush=QColor("black"))
        self.arrow.setZValue(1000)
        self.addItem(self.arrow)

    def init_waypoints(self):
        # Number labels for each waypoint
        self.waypoints_numbers = []

        # Path line
        self.waypoints_line = self.plot([], 
                                        [], 
                                        pen=pg.mkPen('magenta', width=5), 
                                        symbol="o", 
                                        symbolSize=50, 
                                        symbolBrush=QColor("black"), 
                                        symbolPen=pg.mkPen(QColor("magenta"), width=5))
        
        # Create target waypoint
        self.target_marker = pg.ScatterPlotItem([], [], size=100, brush=pg.mkBrush(0, 0, 0, 0), pen=pg.mkPen('white', width=2))
        self.addItem(self.target_marker)

    def update(self, flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg):
        # Update title
        self.setTitle(f"<p style='white-space:pre;'>Lat:{flight_data.lat:.6f}      Lon:{flight_data.lon:.6f}</p>")

        # Update position of aircraft
        position = calculate_displacement_meters(flight_data.lat, flight_data.lon, flight_data.center_lat, flight_data.center_lon)
        self.arrow.setStyle(angle=flight_data.heading + 90)
        self.arrow.setPos(position[0], position[1])

        # Update target waypoint
        x, y = calculate_displacement_meters(waypoints[flight_data.wp_idx][0], waypoints[flight_data.wp_idx][1], flight_data.center_lat, flight_data.center_lon)
        self.target_marker.setData([x], [y])

        # Update runway position
        rwy_e, rwy_n = calculate_displacement_meters(rwy_lat, rwy_lon, flight_data.center_lat, flight_data.center_lon)
        self.rwy_line.setData([rwy_e, rwy_e - 500*math.sin(math.radians(rwy_hdg))], [rwy_n, rwy_n - 500*math.cos(math.radians(rwy_hdg))])
        self.rwy_marker.setData([rwy_e], [rwy_n])

        # Update waypoints
        x = []
        y = []
        for waypoint in waypoints:
            x_pt, y_pt = calculate_displacement_meters(waypoint[0], waypoint[1], flight_data.center_lat, flight_data.center_lon)
            x.append(x_pt)
            y.append(y_pt)
        self.waypoints_line.setData(x, y)

        # Update waypoint number labels
        for i in range(min(len(waypoints), len(self.waypoints_numbers))):
            self.waypoints_numbers[i].setPos(x[i], y[i])
        if len(self.waypoints_numbers) > len(waypoints): # WP has been removed
            for i in range(len(waypoints), len(self.waypoints_numbers)):
                self.removeItem(self.waypoints_numbers[i])
                self.waypoints_numbers.pop(i)
        elif len(waypoints) > len(self.waypoints_numbers): # WP has been added
            for i in range(len(self.waypoints_numbers), len(waypoints)):
                font = QFont()
                font.setPixelSize(40)
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
                text.setPos(x[i], y[i])
                text.setFont(font)
                self.addItem(text)
                self.waypoints_numbers.append(text)