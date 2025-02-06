import pyqtgraph as pg
from PyQt5.QtGui import *
import numpy as np
import math

class AltitudeGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.waypoint_labels = []

        self.line = self.plot([], 
                              [], 
                              pen=pg.mkPen('magenta', width=5), 
                              fillLevel=0, 
                              brush=QColor(255, 0, 255, 50), 
                              symbol="o", 
                              symbolSize=50, 
                              symbolBrush=QColor("black"), 
                              symbolPen=pg.mkPen(QColor("magenta"), width=5))
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.getViewBox().setMouseEnabled(x=False, y=False)
        self.setBackground(QColor("#202124"))
    
    def update(self, waypoints):
        # Update line
        x = [math.sqrt((waypoints[0][0])**2 + (waypoints[0][1])**2)]
        for i in range(1, len(waypoints)):
            # Calculate distance between target and previous waypoints
            wp = waypoints[i]
            prev_wp = waypoints[i - 1]    
            dist = math.sqrt((wp[0] - prev_wp[0])**2 + (wp[1] - prev_wp[1])**2)

            # Add distance to previous distance in array
            x.append(x[i - 1] + dist)
        # All the altitudes
        y = [wp[2]*-1 for wp in waypoints]
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
                font = QFont()
                font.setPixelSize(40)
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
                text.setPos(x[i], y[i])
                text.setFont(font)
                self.addItem(text)
                self.waypoint_labels.append(text)