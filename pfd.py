from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class PrimaryFlightDisplay:
    def __init__(self):
        # Canvas setup
        self.width = 1300
        self.height = 800
        self.canvas = QPixmap(self.width, self.height)
        self.painter = QPainter(self.canvas)

        # Flight data
        self.pitch = 0
        self.roll = 0
        self.pitch_setpoint = 0
        self.roll_setpoint = 0
        self.altitude = 0
        self.speed = 0

        # Wings
        self.wings_width = 8
        self.wings_length = 80
        self.wings_height = 20
        self.wings_starting = self.width/2 - 200

        # Horizon
        self.horizon_thickness = 1

        # Pitch scale
        self.pitch_scale_spacing = 60
        self.pitch_scale_length_big = 200
        self.pitch_scale_length_small = 100
        self.pitch_scale_num = 20
        self.pitch_scale_thickness = 1
        self.pitch_scale_intervals = 5

        # Altitude and speed scale
        self.scale_height = 550
        self.scale_width = 100
        self.scale_offset = 150
        self.tick_length = 15
        self.tick_thickness = 1

        # Speed scale
        self.speed_scale_spacing = 100
        self.speed_scale_n_ticks = 6
        self.speed_scale_intervals = 5

        # Altitude scale
        self.altitude_scale_spacing = 100
        self.altitude_scale_n_ticks = 50
        self.altitude_scale_intervals = 10

        # Flight director
        self.flight_director_thickness = 4
        self.flight_director_length = 150   

    def update(self, pitch, roll, altitude, speed, pitch_setpoint, roll_setpoint):
        # Update flight data
        self.pitch = pitch
        self.roll = -roll
        self.speed = speed
        self.altitude = altitude
        self.pitch_setpoint = pitch_setpoint
        self.roll_setpoint = roll_setpoint

        self.draw_background()
        self.draw_wings()
        self.draw_pitch_scale()
        self.draw_altitude_scale()
        self.draw_speed_scale()
        self.draw_flight_director()

        return self.canvas

    def pitch_deg_to_px(self, deg):
        return deg * (self.pitch_scale_spacing / self.pitch_scale_intervals)

    def speed_to_px(self, speed):
        return speed * (self.speed_scale_spacing / self.speed_scale_intervals)
    
    def altitude_to_px(self, altitude):
        return altitude * (self.altitude_scale_spacing / self.altitude_scale_intervals)

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

        scale_pixmap = QPixmap(self.width, self.height)
        scale_pixmap.fill(Qt.transparent)
        scale_painter = QPainter(scale_pixmap)

        # Mask
        path = QPainterPath()
        path.addRect(self.scale_offset - self.scale_width/2, self.height/2 - self.scale_height/2, self.scale_width, self.scale_height)
        scale_painter.setClipPath(path, Qt.IntersectClip)

        # Tick marks
        scale_painter.setPen(QPen(QColor("white"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.speed_scale_n_ticks):
            offset = i * self.speed_scale_spacing - self.scale_height/2
            x1 = self.scale_offset + self.scale_width/2
            x2 = self.scale_offset + self.scale_width/2 - self.tick_length
            y = self.height/2 - self.scale_height/2 - offset + self.speed_to_px(self.speed)

            scale_painter.drawLine(x1, y, x2, y)
            scale_painter.drawText(QPoint(x1 - 60, y + 10), str(i * self.speed_scale_intervals))

            # If y less than zero, break
        
        scale_painter.end()

        self.painter.drawPixmap(QPoint(), scale_pixmap)

        # Draw black box with speed reading
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))     
        self.draw_rect_center(self.scale_offset, self.height/2, self.scale_width - 20, 50)
        self.painter.drawText(QPoint(self.scale_offset - 10, self.height/2 + 10), str(int(self.speed)))
    
    def draw_altitude_scale(self):
        self.painter.setPen(QPen(QColor("grey"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("grey"), Qt.SolidPattern))
        self.painter.setOpacity(0.5)

        # Grey container
        self.draw_rect_center(self.width - self.scale_offset, self.height/2, self.scale_width, self.scale_height)

        self.painter.setOpacity(1.0)

        scale_pixmap = QPixmap(self.width, self.height)
        scale_pixmap.fill(Qt.transparent)
        scale_painter = QPainter(scale_pixmap)

        # Mask
        path = QPainterPath()
        path.addRect(self.width - self.scale_offset - self.scale_width/2, self.height/2 - self.scale_height/2, self.scale_width, self.scale_height)
        scale_painter.setClipPath(path, Qt.IntersectClip)

        # Tick marks
        scale_painter.setPen(QPen(QColor("white"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.altitude_scale_n_ticks):
            offset = i * self.altitude_scale_spacing - self.scale_height/2
            x1 = self.width - self.scale_offset - self.scale_width/2
            x2 = self.width - self.scale_offset - self.scale_width/2 + self.tick_length
            y = self.height/2 - self.scale_height/2 - offset + self.altitude_to_px(self.altitude)

            scale_painter.drawLine(x1, y, x2, y)
            scale_painter.drawText(QPoint(x1 + 45, y + 10), str(int(i * self.altitude_scale_intervals)))
        
        scale_painter.end()

        self.painter.drawPixmap(QPoint(), scale_pixmap)

        # Draw black box with altitude reading
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))     
        self.draw_rect_center(self.width - self.scale_offset, self.height/2, self.scale_width - 20, 50)
        self.painter.drawText(QPoint(self.width - self.scale_offset - 10, self.height/2 + 10), str(int(abs(self.altitude))))

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

    def draw_pitch_scale(self):
        self.painter.setPen(QPen(QColor("white"), self.pitch_scale_thickness, Qt.SolidLine))

        for i in range(1, self.pitch_scale_num):
            pitch_scale_length = self.pitch_scale_length_small

            if (i % 2 == 0):
                pitch_scale_length = self.pitch_scale_length_big

            origin = (self.width/2, self.height/2)
            height = self.height/2 - i * self.pitch_scale_spacing + self.pitch_deg_to_px(self.pitch)
            point_left = self.rotate_point(origin, (self.width/2 - pitch_scale_length, height), math.radians(self.roll))
            point_right = self.rotate_point(origin, (self.width/2 + pitch_scale_length, height), math.radians(self.roll))
            self.painter.drawLine(point_left[0], point_left[1], point_right[0], point_right[1])

            height = self.height/2 + i * self.pitch_scale_spacing + self.pitch_deg_to_px(self.pitch)
            point_left = self.rotate_point(origin, (self.width/2 - pitch_scale_length, height), math.radians(self.roll))
            point_right = self.rotate_point(origin, (self.width/2 + pitch_scale_length, height), math.radians(self.roll))
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

    def draw_background(self):
        horizon_left = int(self.height/2 - (self.width/2)*math.sin(math.radians(self.roll)) + self.pitch_deg_to_px(self.pitch))
        horizon_right = int(self.height/2 + (self.width/2)*math.sin(math.radians(self.roll)) + self.pitch_deg_to_px(self.pitch))
        
        # Sky
        self.painter.setPen(QPen(QColor("#3478cc"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#3478cc"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygon([QPoint(0, 0),
                                      QPoint(self.width, 0),
                                      QPoint(self.width, horizon_right),
                                      QPoint(0, horizon_left)]))

        # Ground
        self.painter.setPen(QPen(QColor("#6a5200"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#6a5200"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygon([QPoint(0, self.height),
                                      QPoint(self.width, self.height),
                                      QPoint(self.width, horizon_right),
                                      QPoint(0, horizon_left)]))
        
        # Horizon
        self.painter.setPen(QPen(QColor("white"), self.horizon_thickness, Qt.SolidLine))
        self.painter.drawLine(0, horizon_left, self.width, horizon_right)