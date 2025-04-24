import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from utils.utils import calculate_displacement_meters
import math

class AltitudeGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.getViewBox().setMouseEnabled(x=False, y=False)
        self.setBackground(None)
        self.getAxis('left').setStyle(tickFont=pg.QtGui.QFont('Arial', 14))
        self.getAxis('bottom').setStyle(tickFont=pg.QtGui.QFont('Arial', 14))
        self.waypoints = []
        self.current_waypoint_index = None
    
    def set_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.render()
    
    def set_current_waypoint_index(self, index):
        self.current_waypoint_index = index
        self.render()
    
    def render(self):
        self.clear()

        x = [0]
        for i in range(1, len(self.waypoints)):
            wp_pos = calculate_displacement_meters(self.waypoints[i].lat, 
                                                   self.waypoints[i].lon, 
                                                   self.waypoints[0].lat, 
                                                   self.waypoints[0].lon)
            prev_wp_pos = calculate_displacement_meters(self.waypoints[i-1].lat, 
                                                        self.waypoints[i-1].lon, 
                                                        self.waypoints[0].lat, 
                                                        self.waypoints[0].lon)
            dist = math.sqrt((wp_pos[0] - prev_wp_pos[0])**2 + (wp_pos[1] - prev_wp_pos[1])**2)
            x.append(x[i - 1] + dist)
        y = [wp.alt for wp in self.waypoints]
        brush_color = [QColor("black")] * len(x)
        if self.current_waypoint_index and self.current_waypoint_index < len(self.waypoints):
            brush_color[self.current_waypoint_index] = QColor(Qt.magenta)
        self.plot(x, 
                y,
                pen=pg.mkPen('magenta', width=5), 
                fillLevel=0, 
                brush=QColor(255, 0, 255, 50), 
                symbol="o", 
                symbolSize=40, 
                symbolBrush=brush_color, 
                symbolPen=pg.mkPen(QColor("magenta"), width=5))

        # Add waypoint number labels
        for i in range(len(self.waypoints)):
            s = str(i)
            if i == 0:
                s = "H"
            elif i == len(self.waypoints) - 1:
                s = "L"
            text = pg.TextItem(text=s, color=QColor("white"), anchor=(0.5, 0.5))
            text.setFont(QFont("Arial", 10))
            text.setPos(x[i], y[i])
            self.addItem(text)
    
    def keyPressEvent(self, event):
        # Propagate the key press event to the parent widget
        self.parent().keyPressEvent(event)

# Test
if __name__ == "__main__":
    app = QApplication([])

    alt_graph = AltitudeGraph()
    alt_graph.show()

    app.exec()