from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class PrimaryFlightDisplay:
    def __init__(self, width, height):
        # Canvas setup
        self.width = width
        self.height = height
        self.canvas = QPixmap(self.width, self.height)
        self.painter = QPainter(self.canvas)

        # Wings
        self.wings_width = 6
        self.wings_length = 80
        self.wings_height = 20
        self.wings_starting = self.width/2 - 200

        # Pitch scale
        self.pitch_scale_spacing = 50
        self.pitch_scale_length_big = 100
        self.pitch_scale_length_small = 50
        self.pitch_scale_num = 6

        # Altitude and speed scale
        self.scale_height = 550
        self.scale_width = 100
        self.scale_offset = 150
        self.tick_length = 15
        self.tick_thickness = 2
        self.num_ticks = 10

        # Flight director
        self.flight_director_thickness = 4
        self.flight_director_length = 150

    def update(self, pitch, roll, alt, pitch_setpoint, roll_setpoint):
        horizon_left = int(self.height/2 - (self.width/2)*math.sin(math.radians(roll)) + pitch)
        horizon_right = int(self.height/2 + (self.width/2)*math.sin(math.radians(roll)) + pitch)

        self.pitch_setpoint = pitch_setpoint
        self.roll_setpoint = roll_setpoint

        self.draw_sky(horizon_right, horizon_left)
        self.draw_ground(horizon_right, horizon_left)
        self.draw_horizon(horizon_right, horizon_left)
        self.draw_wings()
        self.draw_pitch_scale(math.radians(roll), pitch)
        self.draw_altitude_scale()
        self.draw_speed_scale()
        self.draw_flight_director()

        return self.canvas

    def draw_flight_director(self):
        self.painter.setPen(QPen(QColor("magenta"), self.flight_director_thickness, Qt.SolidLine))
        
        # Horizontal
        self.painter.drawLine(self.width/2 - self.flight_director_length, self.height/2 - self.pitch_setpoint, self.width/2 + self.flight_director_length, self.height/2 - self.pitch_setpoint)

        # Vertical
        self.painter.drawLine(self.width/2 + self.roll_setpoint, self.height/2 - self.flight_director_length - self.pitch_setpoint, self.width/2 + self.roll_setpoint, self.height/2 + self.flight_director_length - self.pitch_setpoint)

    def draw_speed_scale(self):
        self.painter.setPen(QPen(QColor("grey"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("grey"), Qt.SolidPattern))
        self.painter.setOpacity(0.5)

        # Grey container
        self.draw_rect_center(self.scale_offset, self.height/2, self.scale_width, self.scale_height)

        self.painter.setOpacity(1.0)

        # Tick marks
        self.painter.setPen(QPen(QColor("white"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.num_ticks):
            offset = i * self.scale_height / self.num_ticks

            self.painter.drawLine(self.scale_offset + self.scale_width/2, self.height/2 - self.scale_height/2 + offset,
                                  self.scale_offset + self.scale_width/2 - self.tick_length, self.height/2 - self.scale_height/2 + offset)
    
    def draw_altitude_scale(self):
        self.painter.setPen(QPen(QColor("grey"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("grey"), Qt.SolidPattern))
        self.painter.setOpacity(0.5)

        # Grey container
        self.draw_rect_center(self.width - self.scale_offset, self.height/2, self.scale_width, self.scale_height)

        self.painter.setOpacity(1.0)

        # Tick marks
        self.painter.setPen(QPen(QColor("white"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.num_ticks):
            offset = i * self.scale_height / self.num_ticks

            self.painter.drawLine(self.width - self.scale_offset - self.scale_width/2, self.height/2 - self.scale_height/2 + offset,
                                  self.width - self.scale_offset - self.scale_width/2 + self.tick_length, self.height/2 - self.scale_height/2 + offset)

    def draw_rect_center(self, x, y, width, height):
        self.painter.drawRect(x - width/2, y - height/2, width, height)

    def rotate_point(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def draw_pitch_scale(self, roll, pitch):
        for i in range(1, self.pitch_scale_num):
            pitch_scale_length = self.pitch_scale_length_small

            if (i % 2 == 0):
                pitch_scale_length = self.pitch_scale_length_big

            point_left = self.rotate_point((self.width/2, self.height/2), (self.width/2 - pitch_scale_length, self.height/2 - i * self.pitch_scale_spacing + pitch), roll)
            point_right = self.rotate_point((self.width/2, self.height/2), (self.width/2 + pitch_scale_length, self.height/2 - i * self.pitch_scale_spacing + pitch), roll)

            self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
            self.painter.drawLine(point_left[0], point_left[1], point_right[0], point_right[1])

            point_left = self.rotate_point((self.width/2, self.height/2), (self.width/2 - pitch_scale_length, self.height/2 + i * self.pitch_scale_spacing + pitch), roll)
            point_right = self.rotate_point((self.width/2, self.height/2), (self.width/2 + pitch_scale_length, self.height/2 + i * self.pitch_scale_spacing + pitch), roll)

            self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
            self.painter.drawLine(point_left[0], point_left[1], point_right[0], point_right[1])

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