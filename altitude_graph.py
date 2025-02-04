import pyqtgraph as pg
from PyQt5.QtGui import *
import numpy as np
import math

class AltitudeGraph(pg.PlotWidget):
    def __init__(self, waypoints):
        super().__init__()

        self.waypoints = waypoints
        self.waypoint_labels = []

        self.x = [math.sqrt((self.waypoints[0][0])**2 + (self.waypoints[0][1])**2)]
        for i in range(1, len(self.waypoints)):
            wp = self.waypoints[i]
            prev_wp = self.waypoints[i - 1]    
            dist = math.sqrt((wp[0] - prev_wp[0])**2 + (wp[1] - prev_wp[1])**2)
            self.x.append(self.x[i - 1] + dist)
        self.y = [wp[2]*-1 for wp in self.waypoints]

        self.line = self.plot(self.x, 
                  self.y, 
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

        # Add numbers
        for i in range(len(self.x)):
            font = QFont()
            font.setPixelSize(40)
            text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
            text.setPos(self.x[i], self.y[i])
            text.setFont(font)
            self.addItem(text)
            self.waypoint_labels.append(text)
    
    def update(self, waypoints):
        self.waypoints = waypoints

        # Update line
        self.x = [math.sqrt((self.waypoints[0][0])**2 + (self.waypoints[0][1])**2)]
        for i in range(1, len(self.waypoints)):
            wp = self.waypoints[i]
            prev_wp = self.waypoints[i - 1]    
            dist = math.sqrt((wp[0] - prev_wp[0])**2 + (wp[1] - prev_wp[1])**2)
            self.x.append(self.x[i - 1] + dist)
        self.y = [wp[2]*-1 for wp in self.waypoints]
        self.line.setData(self.x, self.y)

        # Update waypoint number labels
        for i in range(min(len(self.waypoints), len(self.waypoint_labels))):
            self.waypoint_labels[i].setPos(self.x[i], self.y[i])

        if len(self.waypoint_labels) > len(self.waypoints): # Removed WP
            for i in range(len(self.waypoints), len(self.waypoint_labels)):
                self.removeItem(self.waypoint_labels[i])
                self.waypoint_labels.pop(i)
        elif len(self.waypoints) > len(self.waypoint_labels): # Added WP
            for i in range(len(self.waypoint_labels), len(self.waypoints)):
                font = QFont()
                font.setPixelSize(40)
                text = pg.TextItem(text=str(i), color=QColor("white"), anchor=(0.5, 0.5))
                text.setPos(self.x[i], self.y[i])
                text.setFont(font)
                self.addItem(text)
                self.waypoint_labels.append(text)