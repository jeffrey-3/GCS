from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QFont, QPen, QColor, QBrush, QPolygonF
from flight_data import FlightData
import math

class PrimaryFlightDisplay(QLabel):
    def __init__(self):
        super().__init__()

        self.flight_data = FlightData()
        
        # Canvas setup
        self.width = 1200
        self.height = 600
        self.canvas = QPixmap(self.width, self.height)
        self.setPixmap(self.canvas)
        self.painter = QPainter(self.canvas)
        self.font = QFont("Arial", 20)  # Set font family and size
        self.painter.setFont(self.font)

        # Wings
        self.wings_center_square_size = 15
        self.wings_width = 10
        self.wings_border_width = 2
        self.wings_length = 100
        self.wings_height = 20
        self.wings_starting = self.width/2 - 250 # How far apart the sides are

        # Horizon
        self.horizon_thickness = 2

        # Pitch scale
        self.pitch_scale_spacing = 70
        self.pitch_scale_length_big = 100
        self.pitch_scale_length_small = 70
        self.pitch_scale_num = 20
        self.pitch_scale_thickness = 2
        self.pitch_scale_intervals = 5

        # Altitude and speed scale
        self.scale_height = 550
        self.scale_width = 180
        self.tick_length = 30
        self.tick_thickness = 4
        self.box_height = 70

        # Speed scale
        self.speed_scale_spacing = 100
        self.speed_scale_n_ticks = 6
        self.speed_scale_intervals = 5

        # Altitude scale
        self.altitude_scale_spacing = 100
        self.altitude_scale_n_ticks = 20
        self.altitude_scale_intervals = 10

        # Flight director
        self.flight_director_thickness = 5
        self.flight_director_length = 170
        self.fd_px_per_hdg_deg = 2

        # Heading scale
        self.hdg_scale_spacing = 150
        self.hdg_scale_length = 30
        self.hdg_tick_interval = 22.5 # Degrees per tick on scale

    def update(self, flight_data):
        self.flight_data = flight_data

        self.draw_background()
        self.draw_pitch_scale()
        self.draw_altitude_scale()
        self.draw_speed_scale()
        self.draw_heading_scale()
        self.draw_wings()
        # self.draw_flight_director()

        self.setPixmap(self.canvas)
    
    def draw_heading_scale(self):
        scale_width = (360 / self.hdg_tick_interval) * self.hdg_scale_spacing
        x_offset = self.width/2 - (self.flight_data.heading / self.hdg_tick_interval) * self.hdg_scale_spacing
        self.draw_hdg_ticks(-scale_width + x_offset)
        self.draw_hdg_ticks(x_offset)
        self.draw_hdg_ticks(scale_width + x_offset)

        # Scale on edge
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        self.painter.drawLine(QPointF(0, self.height - self.tick_thickness/2), QPointF(self.width, self.height - self.tick_thickness/2))

        # Box
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))     
        self.draw_rect_center(self.width/2, self.height - self.box_height/2, self.scale_width, self.box_height)

        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(self.width/2 - self.scale_width/2, self.height - self.box_height, self.scale_width, self.box_height), Qt.AlignCenter, "{:.1f}".format(self.flight_data.heading))

    def draw_hdg_ticks(self, x_offset):
        num_ticks = int(360 / self.hdg_tick_interval)
        self.painter.setPen(QPen(QColor("white"), self.tick_thickness, Qt.SolidLine))
        for i in range(num_ticks):
            x = i * self.hdg_scale_spacing + x_offset
            self.painter.drawLine(QPointF(x, self.height), QPointF(x, self.height - self.hdg_scale_length))

            val = i * self.hdg_tick_interval
            s = ""
            if val == 0:
                s = "N"
            elif val == 90:
                s = "E"
            elif val == 180:
                s = "S"
            elif val == 270:
                s = "W"
            self.painter.drawText(QRectF(x, self.height - self.box_height, self.hdg_scale_spacing, self.box_height), Qt.AlignCenter, s)

    def pitch_deg_to_px(self, deg):
        return deg * (self.pitch_scale_spacing / self.pitch_scale_intervals)

    def speed_to_px(self, speed):
        return speed * (self.speed_scale_spacing / self.speed_scale_intervals)
    
    def altitude_to_px(self, altitude):
        return altitude * (self.altitude_scale_spacing / self.altitude_scale_intervals)

    def draw_flight_director(self):
        # Calculate deviation from setpoints
        pitch_error = self.flight_data.pitch_setpoint - self.flight_data.pitch
        heading_error = self.flight_data.heading_setpoint - self.flight_data.heading

        # Normalize heading error to nearest
        while heading_error >= 180:
            heading_error -= 360
        while heading_error < -180:
            heading_error += 360

        self.painter.setPen(QPen(QColor("magenta"), self.flight_director_thickness, Qt.SolidLine))
        
        # Horizontal
        y = self.height/2 - self.pitch_deg_to_px(pitch_error)
        y = self.clamp(y, 
                       self.height/2 - self.flight_director_length*0.8, 
                       self.height/2 + self.flight_director_length*0.8)
        self.painter.drawLine(QPointF(self.width/2 - self.flight_director_length, y),
                              QPointF(self.width/2 + self.flight_director_length, y))

        # Vertical
        x = self.width/2 + heading_error*self.fd_px_per_hdg_deg
        x = self.clamp(x, 
                       self.width/2 - self.flight_director_length*0.8, 
                       self.width/2 + self.flight_director_length*0.8)
        self.painter.drawLine(QPointF(x, self.height/2 - self.flight_director_length - self.flight_data.pitch_setpoint), 
                              QPointF(x, self.height/2 + self.flight_director_length - self.flight_data.pitch_setpoint))

    def draw_speed_scale(self):
        self.painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        self.painter.setOpacity(0.3)

        # Grey container
        self.painter.drawRect(QRectF(0, 0, self.scale_width, self.height))

        # Tick marks
        self.painter.setOpacity(1.0)
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.speed_scale_n_ticks):
            offset = i * self.speed_scale_spacing - self.scale_height/2
            x1 = 0
            x2 = self.tick_length
            y = self.height/2 - self.scale_height/2 - offset + self.speed_to_px(self.flight_data.speed)

            self.painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            self.painter.drawText(QRectF(self.tick_length + margin, y - self.speed_scale_spacing/2, self.scale_width - self.tick_length, self.speed_scale_spacing), Qt.AlignVCenter | Qt.AlignLeft, str(i * self.speed_scale_intervals))

        self.painter.drawLine(QPointF(self.tick_thickness/2, 0), 
                              QPointF(self.tick_thickness/2, self.height)) # Scale

        # Draw black box with speed reading
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))     
        self.draw_rect_center(self.scale_width/2, self.height/2, self.scale_width- self.tick_thickness, self.box_height)
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(0, self.height/2 - self.box_height/2, self.scale_width, self.box_height), Qt.AlignCenter, "{:.1f}".format(self.flight_data.speed))
    
    def draw_altitude_scale(self):
        self.painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        self.painter.setOpacity(0.3)

        # Grey container
        self.painter.drawRect(QRectF(self.width - self.scale_width, 0, self.width, self.height))

        # Tick marks
        self.painter.setOpacity(1.0)
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        for i in range(self.altitude_scale_n_ticks):
            offset = i * self.altitude_scale_spacing - self.scale_height/2
            x1 = self.width
            x2 = self.width - self.tick_length
            y = self.height/2 - self.scale_height/2 - offset + self.altitude_to_px(self.flight_data.altitude)

            self.painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            self.painter.drawText(QRectF(self.width - self.scale_width, 
                                        y - self.altitude_scale_spacing/2, 
                                        self.scale_width - self.tick_length - margin,
                                        self.altitude_scale_spacing), Qt.AlignVCenter | Qt.AlignRight, str(int(i * self.altitude_scale_intervals)))
        
        self.painter.drawLine(QPointF(self.width - self.tick_thickness/2, 0), QPointF(self.width - self.tick_thickness/2, self.height)) # Scale

        # Draw black box with altitude reading
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.tick_thickness, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))     
        self.draw_rect_center(self.width - self.scale_width/2, self.height/2, self.scale_width - self.tick_thickness, self.box_height)
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(self.width - self.scale_width, self.height/2 - self.box_height/2, self.scale_width, self.box_height), Qt.AlignCenter, "{:.1f}".format(self.flight_data.altitude))

    def draw_rect_center(self, x, y, width, height):
        self.painter.drawRect(QRectF(x - width/2, y - height/2, width, height))

    def rotate_point(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return [qx, qy]

    def draw_pitch_scale(self):
        for i in range(1, self.pitch_scale_num):
            pitch_scale_length = self.pitch_scale_length_small

            # Alternate between small and big pitch scale markers
            if (i % 2 == 0):
                pitch_scale_length = self.pitch_scale_length_big
                self.painter.setPen(QPen(QColor("white"), self.pitch_scale_thickness, Qt.SolidLine))
            else:
                self.painter.setPen(QPen(QColor("#b4b6b4"), self.pitch_scale_thickness, Qt.SolidLine))

            origin = (self.width/2, self.height/2)
            
            height = self.height/2 - i * self.pitch_scale_spacing + self.pitch_deg_to_px(self.flight_data.pitch)
            point_left = self.rotate_point(origin, (self.width/2 - pitch_scale_length, height), -math.radians(self.flight_data.roll))
            point_right = self.rotate_point(origin, (self.width/2 + pitch_scale_length, height), -math.radians(self.flight_data.roll))
            self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))
            
            height = self.height/2 + i * self.pitch_scale_spacing + self.pitch_deg_to_px(self.flight_data.pitch)
            point_left = self.rotate_point(origin, (self.width/2 - pitch_scale_length, height), -math.radians(self.flight_data.roll))
            point_right = self.rotate_point(origin, (self.width/2 + pitch_scale_length, height), -math.radians(self.flight_data.roll))
            self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

    def draw_wings(self):
        self.painter.setPen(QPen(QColor("#f6d210"), self.wings_border_width, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))

        # Left wing
        self.painter.drawPolygon(QPolygonF([QPointF(self.wings_starting, self.height/2 - self.wings_width/2),
                                      QPointF(self.wings_starting + self.wings_length, self.height/2 - self.wings_width/2),
                                      QPointF(self.wings_starting + self.wings_length, self.height/2 + self.wings_height),
                                      QPointF(self.wings_starting + self.wings_length - self.wings_width, self.height/2 + self.wings_height),
                                      QPointF(self.wings_starting + self.wings_length - self.wings_width, self.height/2 + self.wings_width/2),
                                      QPointF(self.wings_starting, self.height/2 + self.wings_width/2)]))
        
        # Right wing
        self.painter.drawPolygon(QPolygonF([QPointF((self.wings_starting - self.width/2) * -1 + self.width/2, self.height/2 - self.wings_width/2),
                                      QPointF((self.wings_starting + self.wings_length - self.width/2) * -1 + self.width/2, self.height/2 - self.wings_width/2),
                                      QPointF((self.wings_starting + self.wings_length - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_height),
                                      QPointF((self.wings_starting + self.wings_length - self.wings_width - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_height),
                                      QPointF((self.wings_starting + self.wings_length - self.wings_width - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_width/2),
                                      QPointF((self.wings_starting - self.width/2) * -1 + self.width/2, self.height/2 + self.wings_width/2)]))
        
        # Center
        self.painter.drawRect(QRectF(self.width/2 - self.wings_center_square_size/2, self.height/2 - self.wings_center_square_size/2, self.wings_center_square_size, self.wings_center_square_size))

    def draw_background(self):
        origin = (self.width/2, self.height/2)
        
        # x point is just for margin to ensure it extends beyond canvas
        original_left = (-1000, self.height/2 + self.pitch_deg_to_px(self.flight_data.pitch))
        original_right = (self.width + 1000, self.height/2 + self.pitch_deg_to_px(self.flight_data.pitch))
        point_left = self.rotate_point(origin, original_left, -math.radians(self.flight_data.roll))
        point_right = self.rotate_point(origin, original_right, -math.radians(self.flight_data.roll))
        
        # Sky
        self.painter.setPen(QPen(QColor("#0079b4"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#0079b4"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygonF([QPointF(0, 0),
                                           QPointF(self.width, 0),
                                           QPointF(point_right[0], point_right[1]),
                                           QPointF(point_left[0], point_left[1])]))

        # Ground
        self.painter.setPen(QPen(QColor("#624408"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#624408"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygonF([QPointF(0, self.height),
                                           QPointF(self.width, self.height),
                                           QPointF(point_right[0], point_right[1]),
                                           QPointF(point_left[0], point_left[1])]))
        
        # Horizon
        self.painter.setPen(QPen(QColor("#b4b6b4"), self.horizon_thickness, Qt.SolidLine))
        self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))
    
    def clamp(self, value, minval, maxval):
        return sorted((minval, value, maxval))[1]