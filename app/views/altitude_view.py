import pyqtgraph as pg
from PyQt5.QtGui import QColor, QFont
from app.utils.utils import calculate_displacement_meters
import math
from app.utils.data_structures import *

class AltitudeGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(250)

        self.waypoint_labels = []

        self.line = self.plot([], 
                              [], 
                              pen=pg.mkPen('magenta', width=5), 
                              fillLevel=0, 
                              brush=QColor(255, 0, 255, 50), 
                              symbol="o", 
                              symbolSize=40, 
                              symbolBrush=QColor("black"), 
                              symbolPen=pg.mkPen(QColor("magenta"), width=5))
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.getViewBox().setMouseEnabled(x=False, y=False)
        self.setBackground(None)
    
    def update(self, waypoints, center_lat, center_lon):
        if len(waypoints) > 0:
            # Update line
            wp_pos = calculate_displacement_meters(waypoints[0].lat, waypoints[0].lon, center_lat, center_lon)
            x = [math.sqrt(wp_pos[0]**2 + wp_pos[1]**2)]
            for i in range(1, len(waypoints)):
                # Calculate distance between target and previous waypoints
                wp_pos = calculate_displacement_meters(waypoints[i].lat, waypoints[i].lon, center_lat, center_lon)
                prev_wp_pos = calculate_displacement_meters(waypoints[i-1].lat, waypoints[i-1].lon, center_lat, center_lon)
                dist = math.sqrt((wp_pos[0] - prev_wp_pos[0])**2 + (wp_pos[1] - prev_wp_pos[1])**2)

                # Add distance to previous distance in array
                x.append(x[i - 1] + dist)
            # All the altitudes
            y = [-wp.alt for wp in waypoints]
            self.line.setData(x, y)

            # Update waypoint number labels
            for i in range(min(len(waypoints), len(self.waypoint_labels))):
                self.waypoint_labels[i].setPos(x[i], y[i])

            if len(self.waypoint_labels) > len(waypoints): # Removed WP
                for i in range(len(waypoints), len(self.waypoint_labels)):
                    self.removeItem(self.waypoint_labels[i])
                    self.waypoint_labels.pop(i)
            elif len(waypoints) > len(self.waypoint_labels): # Added WP
                for i in range(len(self.waypoint_labels), len(waypoints)):
                    s = str(i + 1)
                    if waypoints[i].type == WaypointType.LAND:
                        s = "L"
                    text = pg.TextItem(text=s, color=QColor("white"), anchor=(0.5, 0.5))
                    text.setPos(x[i], y[i])
                    text.setFont(QFont("Arial", 10))
                    self.addItem(text)
                    self.waypoint_labels.append(text)
        else:
            self.line.setData([], [])
            for i in range(len(self.waypoint_labels)):
                self.removeItem(self.waypoint_labels[i])
            self.waypoint_labels = []