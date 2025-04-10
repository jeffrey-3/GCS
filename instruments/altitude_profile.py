import pyqtgraph as pg
from PyQt5.QtGui import QColor, QFont
from utils.utils import calculate_displacement_meters
import math

class AltitudeGraph(pg.PlotWidget):
    def __init__(self, gcs):
        super().__init__()
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=True, y=True)
        self.getViewBox().setMouseEnabled(x=False, y=False)
        self.setBackground(None)
        self.getAxis('left').setStyle(tickFont=pg.QtGui.QFont('Arial', 14))
        self.getAxis('bottom').setStyle(tickFont=pg.QtGui.QFont('Arial', 14))

        self.update(gcs.get_waypoints(), 0)
    
    def update(self, waypoints, wp_idx):
        self.clear()

        x = [0]
        for i in range(1, len(waypoints)):
            wp_pos = calculate_displacement_meters(waypoints[i].lat, waypoints[i].lon, waypoints[0].lat, waypoints[0].lon)
            prev_wp_pos = calculate_displacement_meters(waypoints[i-1].lat, waypoints[i-1].lon, waypoints[0].lat, waypoints[0].lon)
            dist = math.sqrt((wp_pos[0] - prev_wp_pos[0])**2 + (wp_pos[1] - prev_wp_pos[1])**2)
            x.append(x[i - 1] + dist)
        y = [-wp.alt for wp in waypoints]
        brush_color = [QColor("black")] * len(x)
        if wp_idx:
            brush_color[wp_idx] = QColor(139, 0, 139)
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
        for i in range(len(waypoints)):
            s = str(i + 1)
            if i == 0:
                s = "H"
            elif i == len(waypoints) - 1:
                s = "L"
            text = pg.TextItem(text=s, color=QColor("white"), anchor=(0.5, 0.5))
            text.setFont(QFont("Arial", 10))
            text.setPos(x[i], y[i])
            self.addItem(text)
    
    def keyPressEvent(self, event):
        # Propagate the key press event to the parent widget
        self.parent().keyPressEvent(event)