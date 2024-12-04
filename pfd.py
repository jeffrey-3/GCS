from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class PrimaryFlightDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = QPixmap(self.width, self.height)
        self.painter = QPainter(self.canvas)

        self.wings_width = 6
        self.wings_length = 80
        self.wings_height = 20
        self.wings_starting = self.width/2 - 200

    def update(self, pitch, roll):
        horizon_left = int(self.height/2 - (self.width/2)*math.sin(math.radians(roll)) + pitch)
        horizon_right = int(self.height/2 + (self.width/2)*math.sin(math.radians(roll)) + pitch)

        self.draw_sky(horizon_right, horizon_left)
        self.draw_ground(horizon_right, horizon_left)
        self.draw_horizon(horizon_right, horizon_left)
        self.draw_wings()

        return self.canvas

    def draw_wings(self):
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))

        # Left wing
        self.painter.drawPolygon(QPolygon([QPoint(self.wings_starting, self.height/2 - self.wings_width/2),
                                      QPoint(self.wings_starting + self.wings_length, self.height/2 - self.wings_width/2),
                                      QPoint(self.wings_starting + self.wings_length, self.height/2 + self.wings_height),
                                      QPoint(self.wings_starting + self.wings_length - self.wings_width, self.height/2 + self.wings_height),
                                      QPoint(self.wings_starting + self.wings_length - self.wings_width, self.height/2 + self.wings_width/2),
                                      QPoint(self.wings_starting, self.height/2 + self.wings_width/2)]))
        
        # Right wing
        self.painter.drawPolygon(QPolygon([QPoint((self.wings_starting - self.width/2) * -1 + self.width/2, self.height/2 - self.wings_width/2),
                                      QPoint((self.wings_starting + self.wings_length - self.width/2) * -1 + self.width/2, self.height/2 - self.wings_width/2),
                                      QPoint((self.wings_starting + self.wings_length - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_height),
                                      QPoint((self.wings_starting + self.wings_length - self.wings_width - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_height),
                                      QPoint((self.wings_starting + self.wings_length - self.wings_width - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_width/2),
                                      QPoint((self.wings_starting - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_width/2)]))
        
        # Center
        self.painter.drawRect(self.width/2 - self.wings_width/2, self.height/2 - self.wings_width/2, self.wings_width, self.wings_width)
    
    def draw_horizon(self, horizon_right, horizon_left):
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawLine(0, horizon_left, self.width, horizon_right)
    
    def draw_sky(self, horizon_right, horizon_left):
        self.painter.setPen(QPen(QColor("#3478cc"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#3478cc"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygon([QPoint(0, 0),
                                      QPoint(self.width, 0),
                                      QPoint(self.width, horizon_right),
                                      QPoint(0, horizon_left)]))

    def draw_ground(self, horizon_right, horizon_left):
        self.painter.setPen(QPen(QColor("#6a5200"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#6a5200"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygon([QPoint(0, self.height),
                                      QPoint(self.width, self.height),
                                      QPoint(self.width, horizon_right),
                                      QPoint(0, horizon_left)]))