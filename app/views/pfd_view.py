from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

# You can draw pixmap, and then rotate entire pixmap instead of calculating every individual point


class PFDView(QLabel):
    # Canvas
    WIDTH = 1200
    HEIGHT = 600

    # Wings
    WINGS_CENTER_SQUARE_SIZE = 15
    WINGS_WIDTH = 10
    WINGS_BORDER_WIDTH = 2
    WINGS_LENGTH = 100
    WINGS_HEIGHT = 20
    WINGS_STARTING = WIDTH/2 - 250  # How far apart the sides are

    # Horizon
    HORIZON_THICKNESS = 2

    # Pitch scale
    PITCH_SCALE_SPACING = 70
    PITCH_SCALE_LENGTH_BIG = 100
    PITCH_SCALE_LENGTH_SMALL = 70
    PITCH_SCALE_NUM = 18
    PITCH_SCALE_THICKNESS = 2
    PITCH_SCALE_INTERVALS = 5

    # Altitude and speed scale
    SCALE_HEIGHT = 550
    SCALE_WIDTH = 180
    TICK_LENGTH = 30
    TICK_THICKNESS = 4
    BOX_HEIGHT = 70

    # Speed scale
    SPEED_SCALE_SPACING = 100
    SPEED_SCALE_N_TICKS = 20
    SPEED_SCALE_INTERVALS = 2

    # Altitude scale
    ALTITUDE_SCALE_SPACING = 100
    ALTITUDE_SCALE_N_TICKS = 20
    ALTITUDE_SCALE_INTERVALS = 2

    # Flight director
    FLIGHT_DIRECTOR_THICKNESS = 5
    FLIGHT_DIRECTOR_LENGTH = 170
    FD_PX_PER_HDG_DEG = 2

    # Heading scale
    HDG_SCALE_SPACING = 150
    HDG_SCALE_LENGTH = 30
    HDG_TICK_INTERVAL = 22.5  # Degrees per tick on scale

    def __init__(self):
        super().__init__()
        self.canvas = QPixmap(self.WIDTH, self.HEIGHT)
        self.setPixmap(self.canvas)
        self.painter = QPainter(self.canvas)
        self.painter.setFont(QFont("Arial", 20))

    def update(self, roll, pitch, heading, altitude, airspeed):
        self.draw_background(roll, pitch)
        self.draw_pitch_scale(roll, pitch)
        self.draw_altitude_scale(altitude)
        self.draw_speed_scale(airspeed)
        self.draw_heading_scale(heading)
        self.draw_wings()
        # self.draw_flight_director()

        self.setPixmap(self.canvas)

    def draw_heading_scale(self, heading):
        scale_width = (360 / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING
        x_offset = self.WIDTH/2 - (heading / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING
        self.draw_hdg_ticks(-scale_width + x_offset)
        self.draw_hdg_ticks(x_offset)
        self.draw_hdg_ticks(scale_width + x_offset)

        # Scale on edge
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        self.painter.drawLine(QPointF(0, self.HEIGHT - self.TICK_THICKNESS/2), QPointF(self.WIDTH, self.HEIGHT - self.TICK_THICKNESS/2))

        # Box
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))
        self.draw_rect_center(self.WIDTH/2, self.HEIGHT - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT)

        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(self.WIDTH/2 - self.SCALE_WIDTH/2, self.HEIGHT - self.BOX_HEIGHT, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(heading))

    def draw_hdg_ticks(self, x_offset):
        num_ticks = int(360 / self.HDG_TICK_INTERVAL)
        self.painter.setPen(QPen(QColor("white"), self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(num_ticks):
            x = i * self.HDG_SCALE_SPACING + x_offset
            self.painter.drawLine(QPointF(x, self.HEIGHT), QPointF(x, self.HEIGHT - self.HDG_SCALE_LENGTH))

            val = i * self.HDG_TICK_INTERVAL
            s = ""
            if val == 0:
                s = "N"
            elif val == 90:
                s = "E"
            elif val == 180:
                s = "S"
            elif val == 270:
                s = "W"
            self.painter.drawText(QRectF(x, self.HEIGHT - self.BOX_HEIGHT, self.HDG_SCALE_SPACING, self.BOX_HEIGHT), Qt.AlignCenter, s)

    def pitch_deg_to_px(self, deg):
        return deg * (self.PITCH_SCALE_SPACING / self.PITCH_SCALE_INTERVALS)

    def speed_to_px(self, speed):
        return speed * (self.SPEED_SCALE_SPACING / self.SPEED_SCALE_INTERVALS)

    def altitude_to_px(self, altitude):
        return altitude * (self.ALTITUDE_SCALE_SPACING / self.ALTITUDE_SCALE_INTERVALS)

    def draw_flight_director(self):
        # Calculate deviation from setpoints
        pitch_error = self.flight_data.pitch_setpoint - self.flight_data.pitch
        heading_error = self.flight_data.heading_setpoint - self.flight_data.heading

        # Normalize heading error to nearest
        while heading_error >= 180:
            heading_error -= 360
        while heading_error < -180:
            heading_error += 360

        self.painter.setPen(QPen(QColor("magenta"), self.FLIGHT_DIRECTOR_THICKNESS, Qt.SolidLine))

        # Horizontal
        y = self.HEIGHT/2 - self.pitch_deg_to_px(pitch_error)
        y = self.clamp(y,
                       self.HEIGHT/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.HEIGHT/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        self.painter.drawLine(QPointF(self.WIDTH/2 - self.FLIGHT_DIRECTOR_LENGTH, y),
                              QPointF(self.WIDTH/2 + self.FLIGHT_DIRECTOR_LENGTH, y))

        # Vertical
        x = self.WIDTH/2 + heading_error*self.FD_PX_PER_HDG_DEG
        x = self.clamp(x,
                       self.WIDTH/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.WIDTH/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        self.painter.drawLine(QPointF(x, self.HEIGHT/2 - self.FLIGHT_DIRECTOR_LENGTH - self.flight_data.pitch_setpoint),
                              QPointF(x, self.HEIGHT/2 + self.FLIGHT_DIRECTOR_LENGTH - self.flight_data.pitch_setpoint))

    def draw_speed_scale(self, speed):
        self.painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        self.painter.setOpacity(0.3)

        # Grey container
        self.painter.drawRect(QRectF(0, 0, self.SCALE_WIDTH, self.HEIGHT))

        # Tick marks
        self.painter.setOpacity(1.0)
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(self.SPEED_SCALE_N_TICKS):
            offset = i * self.SPEED_SCALE_SPACING - self.SCALE_HEIGHT/2
            x1 = 0
            x2 = self.TICK_LENGTH
            y = self.HEIGHT/2 - self.SCALE_HEIGHT/2 - offset + self.speed_to_px(speed)

            self.painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            self.painter.drawText(QRectF(self.TICK_LENGTH + margin, y - self.SPEED_SCALE_SPACING/2, self.SCALE_WIDTH - self.TICK_LENGTH, self.SPEED_SCALE_SPACING), Qt.AlignVCenter | Qt.AlignLeft, str(i * self.SPEED_SCALE_INTERVALS))

        self.painter.drawLine(QPointF(self.TICK_THICKNESS/2, 0),
                              QPointF(self.TICK_THICKNESS/2, self.HEIGHT))  # Scale

        # Draw black box with speed reading
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))
        self.draw_rect_center(self.SCALE_WIDTH/2, self.HEIGHT/2, self.SCALE_WIDTH - self.TICK_THICKNESS, self.BOX_HEIGHT)
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(0, self.HEIGHT/2 - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(speed))

    def draw_altitude_scale(self, altitude):
        self.painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        self.painter.setOpacity(0.3)

        # Grey container
        self.painter.drawRect(QRectF(self.WIDTH - self.SCALE_WIDTH, 0, self.WIDTH, self.HEIGHT))

        # Tick marks
        self.painter.setOpacity(1.0)
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(self.ALTITUDE_SCALE_N_TICKS):
            offset = i * self.ALTITUDE_SCALE_SPACING - self.SCALE_HEIGHT/2
            x1 = self.WIDTH
            x2 = self.WIDTH - self.TICK_LENGTH
            y = self.HEIGHT/2 - self.SCALE_HEIGHT/2 - offset + self.altitude_to_px(altitude)

            self.painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            self.painter.drawText(QRectF(self.WIDTH - self.SCALE_WIDTH,
                                        y - self.ALTITUDE_SCALE_SPACING/2,
                                        self.SCALE_WIDTH - self.TICK_LENGTH - margin,
                                        self.ALTITUDE_SCALE_SPACING), Qt.AlignVCenter | Qt.AlignRight, str(int(i * self.ALTITUDE_SCALE_INTERVALS)))

        self.painter.drawLine(QPointF(self.WIDTH - self.TICK_THICKNESS/2, 0), QPointF(self.WIDTH - self.TICK_THICKNESS/2, self.HEIGHT))  # Scale

        # Draw black box with altitude reading
        self.painter.setPen(QPen(QColor("#b4b2b4"), self.TICK_THICKNESS, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#383434"), Qt.SolidPattern))
        self.draw_rect_center(self.WIDTH - self.SCALE_WIDTH/2, self.HEIGHT/2, self.SCALE_WIDTH - self.TICK_THICKNESS, self.BOX_HEIGHT)
        self.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        self.painter.drawText(QRectF(self.WIDTH - self.SCALE_WIDTH, self.HEIGHT/2 - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(altitude))

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

    def draw_pitch_scale(self, roll, pitch):
        for i in range(1, self.PITCH_SCALE_NUM):
            pitch_scale_length = self.PITCH_SCALE_LENGTH_SMALL

            # Alternate between small and big pitch scale markers
            if (i % 2 == 0):
                pitch_scale_length = self.PITCH_SCALE_LENGTH_BIG
                self.painter.setPen(QPen(QColor("white"), self.PITCH_SCALE_THICKNESS, Qt.SolidLine))
            else:
                self.painter.setPen(QPen(QColor("#b4b6b4"), self.PITCH_SCALE_THICKNESS, Qt.SolidLine))

            origin = (self.WIDTH/2, self.HEIGHT/2)

            height = self.HEIGHT/2 - i * self.PITCH_SCALE_SPACING + self.pitch_deg_to_px(pitch)
            point_left = self.rotate_point(origin, (self.WIDTH/2 - pitch_scale_length, height), -math.radians(roll))
            point_right = self.rotate_point(origin, (self.WIDTH/2 + pitch_scale_length, height), -math.radians(roll))
            self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

            height = self.HEIGHT/2 + i * self.PITCH_SCALE_SPACING + self.pitch_deg_to_px(pitch)
            point_left = self.rotate_point(origin, (self.WIDTH/2 - pitch_scale_length, height), -math.radians(roll))
            point_right = self.rotate_point(origin, (self.WIDTH/2 + pitch_scale_length, height), -math.radians(roll))
            self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

    def draw_wings(self):
        self.painter.setPen(QPen(QColor("#f6d210"), self.WINGS_BORDER_WIDTH, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))

        # Left wing
        self.painter.drawPolygon(QPolygonF([QPointF(self.WINGS_STARTING, self.HEIGHT/2 - self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH, self.HEIGHT/2 - self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH, self.HEIGHT/2 + self.WINGS_HEIGHT),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH, self.HEIGHT/2 + self.WINGS_HEIGHT),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH, self.HEIGHT/2 + self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING, self.HEIGHT/2 + self.WINGS_WIDTH/2)]))

        # Right wing
        self.painter.drawPolygon(QPolygonF([QPointF((self.WINGS_STARTING - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 - self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 - self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 + self.WINGS_HEIGHT),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 + self.WINGS_HEIGHT),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 + self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING - self.WIDTH/2) * -1 + self.WIDTH/2, self.HEIGHT/2 + self.WINGS_WIDTH/2)]))

        # Center
        self.painter.drawRect(QRectF(self.WIDTH/2 - self.WINGS_CENTER_SQUARE_SIZE/2, self.HEIGHT/2 - self.WINGS_CENTER_SQUARE_SIZE/2, self.WINGS_CENTER_SQUARE_SIZE, self.WINGS_CENTER_SQUARE_SIZE))

    def draw_background(self, roll, pitch):
        origin = (self.WIDTH/2, self.HEIGHT/2)

        # Points of left and right of horizon at 0 pitch and roll
        buffer = 5000
        original_left = (-buffer, self.HEIGHT/2 + self.pitch_deg_to_px(pitch))
        original_right = (self.WIDTH + buffer, self.HEIGHT/2 + self.pitch_deg_to_px(pitch))
        sky_top_left = (original_left[0], original_left[1] - buffer)
        sky_top_right = (original_right[0], original_right[1] - buffer)
        ground_bottom_left = (original_left[0], original_left[1] + buffer)
        ground_bottom_right = (original_right[0], original_right[1] + buffer)

        # Rotate the points for roll
        point_left = self.rotate_point(origin, original_left, -math.radians(roll))
        point_right = self.rotate_point(origin, original_right, -math.radians(roll))
        sky_top_left = self.rotate_point(origin, sky_top_left, -math.radians(roll))
        sky_top_right = self.rotate_point(origin, sky_top_right, -math.radians(roll))
        ground_bottom_left = self.rotate_point(origin, ground_bottom_left, -math.radians(roll))
        ground_bottom_right = self.rotate_point(origin, ground_bottom_right, -math.radians(roll))

        # Sky
        self.painter.setPen(QPen(QColor("#0079b4"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#0079b4"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygonF([QPointF(sky_top_left[0], sky_top_left[1]),
                                            QPointF(sky_top_right[0], sky_top_right[1]),
                                            QPointF(point_right[0], point_right[1]),
                                            QPointF(point_left[0], point_left[1])]))

        # Ground
        self.painter.setPen(QPen(QColor("#624408"), 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(QColor("#624408"), Qt.SolidPattern))
        self.painter.drawPolygon(QPolygonF([QPointF(ground_bottom_left[0], ground_bottom_left[1]),
                                            QPointF(ground_bottom_right[0], ground_bottom_right[1]),
                                            QPointF(point_right[0], point_right[1]),
                                            QPointF(point_left[0], point_left[1])]))

        # Horizon
        self.painter.setPen(QPen(QColor("#b4b6b4"), self.HORIZON_THICKNESS, Qt.SolidLine))
        self.painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

    def clamp(self, value, minval, maxval):
        return sorted((minval, value, maxval))[1]