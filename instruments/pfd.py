from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# Fixed aspect ratio and then use width as size variable to scale 

# make scale red below min speed


class PFDView(QWidget):
    # Colors
    SKY_COLOR = QColor("#0079b4")
    GROUND_COLOR = QColor("#624408")
    LIGHT_GREY = QColor("#b4b2b4")
    DARK_GREY = QColor("#383434")
    YELLOW = QColor("#f6d210")

    # Wings
    WINGS_CENTER_SQUARE_SIZE = 15
    WINGS_WIDTH = 10
    WINGS_BORDER_WIDTH = 2
    WINGS_LENGTH = 100
    WINGS_HEIGHT = 20
    WINGS_STARTING = 250  # How far apart the sides are

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
    FD_PX_PER_ROLL_DEG = 10

    # Heading scale
    HDG_SCALE_SPACING = 150
    HDG_SCALE_LENGTH = 30
    HDG_TICK_INTERVAL = 22.5  # Degrees per tick on scale

    def __init__(self, radio):
        super().__init__()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.altitude = 0
        self.airspeed = 0

        radio.vfr_hud_signal.connect(self.update_values)

    def update_values(self, roll, pitch, heading, altitude, airspeed):
        self.roll = roll
        self.pitch = pitch
        self.heading = heading
        self.altitude = altitude
        self.airspeed = airspeed
        self.update() # Trigger paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 20))

        self.draw_background(painter, self.roll, self.pitch)
        self.draw_pitch_scale(painter, self.roll, self.pitch)
        self.draw_altitude_scale(painter, self.altitude, 20)
        self.draw_speed_scale(painter, self.airspeed, 10)
        self.draw_heading_scale(painter, self.heading)
        self.draw_wings(painter)
        # self.draw_flight_director(painter, self.roll, self.pitch, 0, 0)

        painter.end()

    def draw_heading_scale(self, painter, heading):
        if heading < 0:
            heading += 360

        scale_width = (360 / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING
        x_offset = self.size().width()/2 - (heading / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING
        self.draw_hdg_ticks(painter, -scale_width + x_offset)
        self.draw_hdg_ticks(painter, x_offset)
        self.draw_hdg_ticks(painter, scale_width + x_offset)

        # Scale on edge
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.drawLine(QPointF(0, self.size().height() - self.TICK_THICKNESS/2), QPointF(self.size().width(), self.size().height() - self.TICK_THICKNESS/2))

        # Box
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.setBrush(QBrush(self.DARK_GREY, Qt.SolidPattern))
        self.draw_rect_center(painter, self.size().width()/2, self.size().height() - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT)

        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(self.size().width()/2 - self.SCALE_WIDTH/2, self.size().height() - self.BOX_HEIGHT, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(heading))

    def draw_hdg_ticks(self, painter, x_offset):
        num_ticks = int(360 / self.HDG_TICK_INTERVAL)
        painter.setPen(QPen(QColor("white"), self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(num_ticks):
            x = i * self.HDG_SCALE_SPACING + x_offset
            painter.drawLine(QPointF(x, self.size().height()), QPointF(x, self.size().height() - self.HDG_SCALE_LENGTH))

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
            painter.drawText(QRectF(x, self.size().height() - self.BOX_HEIGHT, self.HDG_SCALE_SPACING, self.BOX_HEIGHT), Qt.AlignCenter, s)

    def pitch_deg_to_px(self, deg):
        return deg * (self.PITCH_SCALE_SPACING / self.PITCH_SCALE_INTERVALS)

    def speed_to_px(self, speed):
        return speed * (self.SPEED_SCALE_SPACING / self.SPEED_SCALE_INTERVALS)

    def altitude_to_px(self, altitude):
        return altitude * (self.ALTITUDE_SCALE_SPACING / self.ALTITUDE_SCALE_INTERVALS)

    def draw_flight_director(self, painter, roll, pitch, roll_setpoint, pitch_setpoint):
        # Calculate deviation from setpoints
        pitch_error = pitch_setpoint - pitch
        roll_error = roll_setpoint - roll

        painter.setPen(QPen(QColor("magenta"), self.FLIGHT_DIRECTOR_THICKNESS, Qt.SolidLine))

        # Horizontal
        y = self.size().height()/2 - self.pitch_deg_to_px(pitch_error)
        y = self.clamp(y,
                       self.size().height()/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.size().height()/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        painter.drawLine(QPointF(self.size().width()/2 - self.FLIGHT_DIRECTOR_LENGTH, y),
                              QPointF(self.size().width()/2 + self.FLIGHT_DIRECTOR_LENGTH, y))

        # Vertical
        x = self.size().width()/2 + roll_error*self.FD_PX_PER_ROLL_DEG
        x = self.clamp(x,
                       self.size().width()/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.size().width()/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        painter.drawLine(QPointF(x, self.size().height()/2 - self.FLIGHT_DIRECTOR_LENGTH - pitch_setpoint),
                              QPointF(x, self.size().height()/2 + self.FLIGHT_DIRECTOR_LENGTH - pitch_setpoint))

    def draw_speed_scale(self, painter, speed, setpoint):
        painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        painter.setOpacity(0.3)

        # Grey container
        painter.drawRect(QRectF(0, 0, self.SCALE_WIDTH, self.size().height()))

        # Tick marks
        painter.setOpacity(1.0)
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(self.SPEED_SCALE_N_TICKS):
            offset = i * self.SPEED_SCALE_SPACING - self.size().height()/2
            x1 = 0
            x2 = self.TICK_LENGTH
            y = -offset + self.speed_to_px(speed)

            painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            painter.drawText(QRectF(self.TICK_LENGTH + margin, y - self.SPEED_SCALE_SPACING/2, self.SCALE_WIDTH - self.TICK_LENGTH, self.SPEED_SCALE_SPACING), Qt.AlignVCenter | Qt.AlignLeft, str(i * self.SPEED_SCALE_INTERVALS))

        painter.drawLine(QPointF(self.TICK_THICKNESS/2, 0),
                              QPointF(self.TICK_THICKNESS/2, self.size().height()))  # Scale
        
        # Speed setpoint
        triangle_width = 20
        triangle_height = 20
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.magenta))
        first_point = QPoint(self.SCALE_WIDTH, self.size().height() / 2 + self.speed_to_px(speed) - self.speed_to_px(setpoint))
        if first_point.y() < triangle_height:
            first_point.setY(triangle_height)
        if first_point.y() > self.size().height() - triangle_height:
            first_point.setY(self.size().height() - triangle_height)
        points = QPolygon([first_point, 
                          QPoint(first_point.x() + triangle_width, first_point.y() + triangle_height),
                          QPoint(first_point.x() + triangle_width, first_point.y() - triangle_height)])
        painter.drawPolygon(points)

        # Draw black box with speed reading
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.setBrush(QBrush(self.DARK_GREY, Qt.SolidPattern))
        self.draw_rect_center(painter, self.SCALE_WIDTH/2, self.size().height()/2, self.SCALE_WIDTH - self.TICK_THICKNESS, self.BOX_HEIGHT)
        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(0, self.size().height()/2 - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(speed))

    def draw_altitude_scale(self, painter, altitude, setpoint):
        painter.setPen(QPen(QColor("black"), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        painter.setOpacity(0.3)

        # Grey container
        painter.drawRect(QRectF(self.size().width() - self.SCALE_WIDTH, 0, self.size().width(), self.size().height()))

        # Tick marks
        painter.setOpacity(1.0)
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(self.ALTITUDE_SCALE_N_TICKS):
            offset = i * self.ALTITUDE_SCALE_SPACING - self.size().height()/2
            x1 = self.size().width()
            x2 = self.size().width() - self.TICK_LENGTH
            y = -offset + self.altitude_to_px(altitude)

            painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            margin = 30
            painter.drawText(QRectF(self.size().width() - self.SCALE_WIDTH,
                                        y - self.ALTITUDE_SCALE_SPACING/2,
                                        self.SCALE_WIDTH - self.TICK_LENGTH - margin,
                                        self.ALTITUDE_SCALE_SPACING), Qt.AlignVCenter | Qt.AlignRight, str(int(i * self.ALTITUDE_SCALE_INTERVALS)))

        painter.drawLine(QPointF(self.size().width() - self.TICK_THICKNESS/2, 0), 
                              QPointF(self.size().width() - self.TICK_THICKNESS/2, self.size().height()))  # Scale
        
        # Setpoint
        triangle_width = 20
        triangle_height = 20
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.magenta))
        first_point = QPoint(self.size().width() - self.SCALE_WIDTH, self.size().height() / 2 + self.altitude_to_px(altitude) - self.altitude_to_px(setpoint))
        if first_point.y() < triangle_height:
            first_point.setY(triangle_height)
        if first_point.y() > self.size().height() - triangle_height:
            first_point.setY(self.size().height() - triangle_height)
        points = QPolygon([first_point, 
                          QPoint(first_point.x() - triangle_width, first_point.y() + triangle_height),
                          QPoint(first_point.x() - triangle_width, first_point.y() - triangle_height)])
        painter.drawPolygon(points)

        # Draw black box with altitude reading
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.setBrush(QBrush(self.DARK_GREY, Qt.SolidPattern))
        self.draw_rect_center(painter, self.size().width() - self.SCALE_WIDTH/2, self.size().height()/2, self.SCALE_WIDTH - self.TICK_THICKNESS, self.BOX_HEIGHT)
        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(self.size().width() - self.SCALE_WIDTH, self.size().height()/2 - self.BOX_HEIGHT/2, self.SCALE_WIDTH, self.BOX_HEIGHT), Qt.AlignCenter, "{:.1f}".format(altitude))

    def draw_rect_center(self, painter, x, y, width, height):
        painter.drawRect(QRectF(x - width/2, y - height/2, width, height))

    def draw_pitch_scale(self, painter, roll, pitch):
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center())
        painter.rotate(-roll) # Test
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center() * -1)

        for i in range(1, self.PITCH_SCALE_NUM):
            pitch_scale_length = self.PITCH_SCALE_LENGTH_SMALL

            # Alternate between small and big pitch scale markers
            if (i % 2 == 0):
                pitch_scale_length = self.PITCH_SCALE_LENGTH_BIG
                painter.setPen(QPen(QColor("white"), self.PITCH_SCALE_THICKNESS, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.LIGHT_GREY, self.PITCH_SCALE_THICKNESS, Qt.SolidLine))

            height = self.size().height()/2 - i * self.PITCH_SCALE_SPACING + self.pitch_deg_to_px(pitch)
            point_left = (self.size().width()/2 - pitch_scale_length, height)
            point_right = (self.size().width()/2 + pitch_scale_length, height)
            painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

            if i % 2 == 0:
                horizontal_offset = 50
                text_height = 100
                text_width = 100
                painter.setFont(QFont("Arial", 15))
                painter.drawText(QRectF(point_left[0] - text_width/2 - horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(i * self.PITCH_SCALE_INTERVALS))
                painter.drawText(QRectF(point_right[0] - text_width/2 + horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(i * self.PITCH_SCALE_INTERVALS))
                painter.setFont(QFont("Arial", 20))

            height = self.size().height()/2 + i * self.PITCH_SCALE_SPACING + self.pitch_deg_to_px(pitch)
            point_left = (self.size().width()/2 - pitch_scale_length, height)
            point_right = (self.size().width()/2 + pitch_scale_length, height)
            painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

            if i % 2 == 0:
                horizontal_offset = 50
                text_height = 100
                text_width = 100
                painter.setFont(QFont("Arial", 15))
                painter.drawText(QRectF(point_left[0] - text_width/2 - horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(-i * self.PITCH_SCALE_INTERVALS))
                painter.drawText(QRectF(point_right[0] - text_width/2 + horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(-i * self.PITCH_SCALE_INTERVALS))
                painter.setFont(QFont("Arial", 20))
    
        painter.resetTransform()

    def draw_wings(self, painter):
        painter.setPen(QPen(self.YELLOW, self.WINGS_BORDER_WIDTH, Qt.SolidLine))
        painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))

        # Left wing
        painter.drawPolygon(QPolygonF([QPointF(self.WINGS_STARTING, self.size().height()/2 - self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH, self.size().height()/2 - self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH, self.size().height()/2 + self.WINGS_HEIGHT),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH, self.size().height()/2 + self.WINGS_HEIGHT),
                                      QPointF(self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH, self.size().height()/2 + self.WINGS_WIDTH/2),
                                      QPointF(self.WINGS_STARTING, self.size().height()/2 + self.WINGS_WIDTH/2)]))

        # Right wing
        painter.drawPolygon(QPolygonF([QPointF((self.WINGS_STARTING - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 - self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 - self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 + self.WINGS_HEIGHT),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 + self.WINGS_HEIGHT),
                                      QPointF((self.WINGS_STARTING + self.WINGS_LENGTH - self.WINGS_WIDTH - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 + self.WINGS_WIDTH/2),
                                      QPointF((self.WINGS_STARTING - self.size().width()/2) * -1 + self.size().width()/2, self.size().height()/2 + self.WINGS_WIDTH/2)]))

        # Center
        painter.drawRect(QRectF(self.size().width()/2 - self.WINGS_CENTER_SQUARE_SIZE/2, self.size().height()/2 - self.WINGS_CENTER_SQUARE_SIZE/2, self.WINGS_CENTER_SQUARE_SIZE, self.WINGS_CENTER_SQUARE_SIZE))

    def draw_background(self, painter, roll, pitch):
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center())
        painter.rotate(-roll) # Test
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center() * -1)

        buffer = 5000 # Extend beyond window to make sure it covers completely
        point_left = (-buffer, self.size().height()/2 + self.pitch_deg_to_px(pitch))
        point_right = (self.size().width() + buffer, self.size().height()/2 + self.pitch_deg_to_px(pitch))
        sky_top_left = (point_left[0], point_left[1] - buffer)
        sky_top_right = (point_right[0], point_right[1] - buffer)
        ground_bottom_left = (point_left[0], point_left[1] + buffer)
        ground_bottom_right = (point_right[0], point_right[1] + buffer)

        # Sky
        painter.setPen(QPen(self.SKY_COLOR, 1, Qt.SolidLine))
        painter.setBrush(QBrush(self.SKY_COLOR, Qt.SolidPattern))
        painter.drawPolygon(QPolygonF([QPointF(sky_top_left[0], sky_top_left[1]),
                                            QPointF(sky_top_right[0], sky_top_right[1]),
                                            QPointF(point_right[0], point_right[1]),
                                            QPointF(point_left[0], point_left[1])]))

        # Ground
        painter.setPen(QPen(self.GROUND_COLOR, 1, Qt.SolidLine))
        painter.setBrush(QBrush(self.GROUND_COLOR, Qt.SolidPattern))
        painter.drawPolygon(QPolygonF([QPointF(ground_bottom_left[0], ground_bottom_left[1]),
                                            QPointF(ground_bottom_right[0], ground_bottom_right[1]),
                                            QPointF(point_right[0], point_right[1]),
                                            QPointF(point_left[0], point_left[1])]))

        # Horizon
        painter.setPen(QPen(self.LIGHT_GREY, self.HORIZON_THICKNESS, Qt.SolidLine))
        painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

        painter.resetTransform()

    def clamp(self, value, minval, maxval):
        return sorted((minval, value, maxval))[1]