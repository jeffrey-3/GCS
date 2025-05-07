from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from aplink.aplink_messages import *
from gcs import GCS

# Fixed aspect ratio and then use width as size variable to scale 

# make scale red below min speed


class PFDView(QWidget):
    FONT_SIZE_LARGE = 0.04
    FONT_SIZE_SMALL = 0.03

    # Colors
    SKY_COLOR = QColor("#0079b4")
    GROUND_COLOR = QColor("#624408")
    LIGHT_GREY = QColor("#b4b2b4")
    DARK_GREY = QColor("#383434")
    YELLOW = QColor("#f6d210")

    # Wings
    WINGS_CENTER_SQUARE_SIZE = 0.015
    WINGS_WIDTH = 0.01
    WINGS_BORDER_WIDTH = 2
    WINGS_LENGTH = 0.1
    WINGS_HEIGHT = 0.02
    WINGS_STARTING = 0.3

    # Horizon
    HORIZON_THICKNESS = 2

    SETPOINT_BUG_SIZE = 0.02

    # Pitch scale
    PITCH_SCALE_SPACING = 0.07
    PITCH_SCALE_LENGTH_BIG = 0.1
    PITCH_SCALE_LENGTH_SMALL = 0.07
    PITCH_SCALE_NUM = 18
    PITCH_SCALE_THICKNESS = 2
    PITCH_SCALE_INTERVALS = 5

    # Altitude and speed scale
    SCALE_WIDTH = 0.18
    TICK_LENGTH = 0.03
    TICK_THICKNESS = 2
    BOX_HEIGHT = 0.07

    # Speed scale
    SPEED_SCALE_SPACING = 0.1
    SPEED_SCALE_N_TICKS = 20
    SPEED_SCALE_INTERVALS = 2

    # Altitude scale
    ALTITUDE_SCALE_SPACING = 0.1
    ALTITUDE_SCALE_N_TICKS = 20
    ALTITUDE_SCALE_INTERVALS = 2

    # Flight director
    FLIGHT_DIRECTOR_THICKNESS = 5
    FLIGHT_DIRECTOR_LENGTH = 170
    FD_PX_PER_ROLL_DEG = 10

    # Heading scale
    HDG_SCALE_SPACING = 0.2
    HDG_SCALE_LENGTH = 0.03
    HDG_TICK_INTERVAL = 22.5  # Degrees per tick on scale

    def __init__(self, gcs: GCS):
        super().__init__()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.altitude = 0
        self.airspeed = 0

        gcs.vehicle_status_full_signal.connect(self.update_vehicle_status_full)

    def update_vehicle_status_full(self, vehicle_status: aplink_vehicle_status_full):
        self.roll = vehicle_status.roll
        self.pitch = vehicle_status.pitch
        self.heading = vehicle_status.yaw
        self.altitude = vehicle_status.alt
        self.airspeed = vehicle_status.spd
        self.update() # Trigger paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setFont(QFont("Arial", int(self.FONT_SIZE_LARGE * self.size().width())))

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

        scale_width = (360 / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING * self.size().width()
        x_offset = self.size().width()/2 - (heading / self.HDG_TICK_INTERVAL) * self.HDG_SCALE_SPACING * self.size().width()
        self.draw_hdg_ticks(painter, -scale_width + x_offset)
        self.draw_hdg_ticks(painter, x_offset)
        self.draw_hdg_ticks(painter, scale_width + x_offset)

        # Scale on edge
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.drawLine(QPointF(0, self.size().height() - self.TICK_THICKNESS/2), QPointF(self.size().width(), self.size().height() - self.TICK_THICKNESS/2))

        # Box
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        painter.setBrush(QBrush(self.DARK_GREY, Qt.SolidPattern))
        self.draw_rect_center(painter, self.size().width()/2, self.size().height() - self.BOX_HEIGHT * self.size().width()/2 - self.TICK_THICKNESS / 2, self.SCALE_WIDTH * self.size().width(), self.BOX_HEIGHT * self.size().width())

        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(self.size().width()/2 - self.SCALE_WIDTH * self.size().width()/2, self.size().height() - self.BOX_HEIGHT * self.size().width(), self.SCALE_WIDTH * self.size().width(), self.BOX_HEIGHT * self.size().width()), Qt.AlignCenter, "{:.1f}".format(heading))

    def draw_hdg_ticks(self, painter, x_offset):
        num_ticks = int(360 / self.HDG_TICK_INTERVAL)
        painter.setPen(QPen(QColor("white"), self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(num_ticks):
            x = i * self.HDG_SCALE_SPACING * self.size().width() + x_offset
            painter.drawLine(QPointF(x, self.size().height()), QPointF(x, self.size().height() - self.HDG_SCALE_LENGTH * self.size().width()))

            val = i * self.HDG_TICK_INTERVAL
            s = ""
            if val == 0:
                s = "N"
            elif val == 45:
                s = "NE"
            elif val == 90:
                s = "E"
            elif val == 135:
                s = "SE"
            elif val == 180:
                s = "S"
            elif val == 225:
                s = "SW"
            elif val == 270:
                s = "W"
            elif val == 315:
                s = "NW"
            painter.drawText(QRectF(x, self.size().height() - self.BOX_HEIGHT * self.size().width(), self.HDG_SCALE_SPACING * self.size().width() / 1.5, self.BOX_HEIGHT * self.size().width()), Qt.AlignVCenter | Qt.AlignLeft, s)

    def pitch_deg_to_px(self, deg):
        return deg * (self.PITCH_SCALE_SPACING * self.size().width() / self.PITCH_SCALE_INTERVALS)

    def speed_to_px(self, speed):
        return speed * (self.SPEED_SCALE_SPACING * self.size().width() / self.SPEED_SCALE_INTERVALS)

    def altitude_to_px(self, altitude):
        return altitude * (self.ALTITUDE_SCALE_SPACING * self.size().width() / self.ALTITUDE_SCALE_INTERVALS)

    def draw_flight_director(self, painter, roll, pitch, roll_setpoint, pitch_setpoint):
        # Calculate deviation from setpoints
        pitch_error = pitch_setpoint - pitch
        roll_error = roll_setpoint - roll

        painter.setPen(QPen(QColor("magenta"), self.FLIGHT_DIRECTOR_THICKNESS, Qt.SolidLine))

        # Horizontal
        y = self.clamp(self.size().height()/2 - self.pitch_deg_to_px(pitch_error),
                       self.size().height()/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.size().height()/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        painter.drawLine(QPointF(self.size().width()/2 - self.FLIGHT_DIRECTOR_LENGTH, y),
                              QPointF(self.size().width()/2 + self.FLIGHT_DIRECTOR_LENGTH, y))

        # Vertical
        x = self.clamp(self.size().width()/2 + roll_error*self.FD_PX_PER_ROLL_DEG,
                       self.size().width()/2 - self.FLIGHT_DIRECTOR_LENGTH*0.8,
                       self.size().width()/2 + self.FLIGHT_DIRECTOR_LENGTH*0.8)
        painter.drawLine(QPointF(x, self.size().height()/2 - self.FLIGHT_DIRECTOR_LENGTH - pitch_setpoint),
                              QPointF(x, self.size().height()/2 + self.FLIGHT_DIRECTOR_LENGTH - pitch_setpoint))

    def draw_speed_scale(self, painter: QPainter, speed, setpoint):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        painter.setOpacity(0.3)

        # Grey container
        painter.drawRect(QRectF(0, 0, self.SCALE_WIDTH * self.size().width(), self.size().height()))

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.red))
        painter.setOpacity(0.2)
        painter.drawRect(0, self.size().height() / 2 + self.speed_to_px(speed), self.SCALE_WIDTH * self.size().width(), self.size().height())
        painter.setOpacity(1)

        # Tick marks
        painter.setOpacity(1.0)
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(-self.SPEED_SCALE_N_TICKS, self.SPEED_SCALE_N_TICKS):
            offset = i * self.SPEED_SCALE_SPACING * self.size().width() - self.size().height()/2
            x1 = 0
            x2 = self.TICK_LENGTH * self.size().width()
            y = -offset + self.speed_to_px(speed)

            painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            mark = i * self.SPEED_SCALE_INTERVALS
            if abs(mark) < 10:
                mark = f"\u00A0{mark}"
            painter.drawText(QRectF(self.TICK_LENGTH * self.size().width(), 
                             y - self.SPEED_SCALE_SPACING * self.size().width() / 2, 
                             self.SCALE_WIDTH * self.size().width() - self.TICK_LENGTH * self.size().width(), 
                             self.SPEED_SCALE_SPACING * self.size().width()), 
                             Qt.AlignCenter, str(mark))

        painter.drawLine(QPointF(self.TICK_THICKNESS/2, 0),
                              QPointF(self.TICK_THICKNESS/2, self.size().height()))  # Scale
        
        # Speed setpoint
        triangle_width = self.SETPOINT_BUG_SIZE * self.size().width()
        triangle_height = self.SETPOINT_BUG_SIZE * self.size().width()
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.magenta))
        first_point = QPoint(self.SCALE_WIDTH * self.size().width(), self.size().height() / 2 + self.speed_to_px(speed) - self.speed_to_px(setpoint))
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
        self.draw_rect_center(painter, self.SCALE_WIDTH * self.size().width()/2, self.size().height()/2, self.SCALE_WIDTH * self.size().width() - self.TICK_THICKNESS, self.BOX_HEIGHT * self.size().width())
        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(0, self.size().height()/2 - self.BOX_HEIGHT * self.size().width()/2, self.SCALE_WIDTH * self.size().width(), self.BOX_HEIGHT * self.size().width()), Qt.AlignCenter, "{:.1f}".format(speed))

    def draw_altitude_scale(self, painter, altitude, setpoint):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("black"), Qt.SolidPattern))
        painter.setOpacity(0.3)

        # Grey container
        painter.drawRect(QRectF(self.size().width() - self.SCALE_WIDTH * self.size().width(), 0, self.size().width(), self.size().height()))

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.red))
        painter.setOpacity(0.2)
        painter.drawRect(self.size().width() - self.SCALE_WIDTH * self.size().width(), 
                         self.size().height() / 2 + self.altitude_to_px(altitude), 
                         self.SCALE_WIDTH * self.size().width(), 
                         self.size().height())
        painter.setOpacity(1)

        # Tick marks
        painter.setOpacity(1.0)
        painter.setPen(QPen(self.LIGHT_GREY, self.TICK_THICKNESS, Qt.SolidLine))
        for i in range(-self.ALTITUDE_SCALE_N_TICKS, self.ALTITUDE_SCALE_N_TICKS):
            offset = i * self.ALTITUDE_SCALE_SPACING * self.size().width() - self.size().height()/2
            x1 = self.size().width()
            x2 = self.size().width() - self.TICK_LENGTH * self.size().width()
            y = -offset + self.altitude_to_px(altitude)

            painter.drawLine(QPointF(x1, y), QPointF(x2, y))

            mark = int(i * self.ALTITUDE_SCALE_INTERVALS)
            if abs(mark) < 10:
                mark = f"\u00A0{mark}"
            painter.drawText(QRectF(self.TICK_LENGTH * self.size().width(), 
                             y - self.SPEED_SCALE_SPACING * self.size().width() / 2, 
                             self.SCALE_WIDTH * self.size().width() - self.TICK_LENGTH * self.size().width(), 
                             self.SPEED_SCALE_SPACING * self.size().width()), 
                             Qt.AlignCenter, str(mark))
            painter.drawText(QRectF(self.size().width() - self.SCALE_WIDTH * self.size().width(),
                                        y - self.ALTITUDE_SCALE_SPACING * self.size().width()/2,
                                        self.SCALE_WIDTH * self.size().width() - self.TICK_LENGTH * self.size().width(),
                                        self.ALTITUDE_SCALE_SPACING * self.size().width()), 
                                        Qt.AlignCenter, 
                                        str(mark))

        painter.drawLine(QPointF(self.size().width() - self.TICK_THICKNESS/2, 0), 
                              QPointF(self.size().width() - self.TICK_THICKNESS/2, self.size().height()))  # Scale
        
        # Setpoint
        triangle_width = self.SETPOINT_BUG_SIZE * self.size().width()
        triangle_height = self.SETPOINT_BUG_SIZE * self.size().width()
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.magenta))
        first_point = QPoint(self.size().width() - self.SCALE_WIDTH * self.size().width(), self.size().height() / 2 + self.altitude_to_px(altitude) - self.altitude_to_px(setpoint))
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
        self.draw_rect_center(painter, self.size().width() - self.SCALE_WIDTH * self.size().width()/2, self.size().height()/2, self.SCALE_WIDTH * self.size().width() - self.TICK_THICKNESS, self.BOX_HEIGHT * self.size().width())
        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
        painter.drawText(QRectF(self.size().width() - self.SCALE_WIDTH * self.size().width(), 
                                self.size().height()/2 - self.BOX_HEIGHT * self.size().width()/2, 
                                self.SCALE_WIDTH * self.size().width(), 
                                self.BOX_HEIGHT * self.size().width()), 
                                Qt.AlignCenter, "{:.1f}".format(altitude))

    def draw_rect_center(self, painter, x, y, width, height):
        painter.drawRect(QRectF(x - width/2, y - height/2, width, height))

    def draw_pitch_scale(self, painter, roll, pitch):
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center())
        painter.rotate(-roll) # Test
        painter.translate(QRectF(0, 0, self.size().width(), self.size().height()).center() * -1)

        for i in range(1, self.PITCH_SCALE_NUM):
            pitch_scale_length = self.PITCH_SCALE_LENGTH_SMALL * self.size().width()

            # Alternate between small and big pitch scale markers
            if (i % 2 == 0):
                pitch_scale_length = self.PITCH_SCALE_LENGTH_BIG * self.size().width()
                painter.setPen(QPen(QColor("white"), self.PITCH_SCALE_THICKNESS, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.LIGHT_GREY, self.PITCH_SCALE_THICKNESS, Qt.SolidLine))

            height = self.size().height()/2 - i * self.PITCH_SCALE_SPACING * self.size().width() + self.pitch_deg_to_px(pitch)
            point_left = (self.size().width()/2 - pitch_scale_length, height)
            point_right = (self.size().width()/2 + pitch_scale_length, height)
            painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

            if i % 2 == 0:
                horizontal_offset = 50
                text_height = 100
                text_width = 100
                painter.setFont(QFont("Arial", int(self.FONT_SIZE_SMALL * self.size().width())))
                painter.drawText(QRectF(point_left[0] - text_width/2 - horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(i * self.PITCH_SCALE_INTERVALS))
                painter.drawText(QRectF(point_right[0] - text_width/2 + horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(i * self.PITCH_SCALE_INTERVALS))
                painter.setFont(QFont("Arial", int(self.FONT_SIZE_LARGE * self.size().width())))

            height = self.size().height()/2 + i * self.PITCH_SCALE_SPACING * self.size().width() + self.pitch_deg_to_px(pitch)
            point_left = (self.size().width()/2 - pitch_scale_length, height)
            point_right = (self.size().width()/2 + pitch_scale_length, height)
            painter.drawLine(QPointF(point_left[0], point_left[1]), QPointF(point_right[0], point_right[1]))

            if i % 2 == 0:
                horizontal_offset = 50
                text_height = 100
                text_width = 100
                painter.setFont(QFont("Arial", int(self.FONT_SIZE_SMALL * self.size().width())))
                painter.drawText(QRectF(point_left[0] - text_width/2 - horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(-i * self.PITCH_SCALE_INTERVALS))
                painter.drawText(QRectF(point_right[0] - text_width/2 + horizontal_offset, point_left[1] - text_height/2, 100, 100), Qt.AlignCenter, str(-i * self.PITCH_SCALE_INTERVALS))
                painter.setFont(QFont("Arial", int(self.FONT_SIZE_LARGE * self.size().width())))
    
        painter.resetTransform()

    def draw_wings(self, painter: QPainter):
        wing_points = [
            QPointF(self.WINGS_STARTING * self.size().width(), self.size().height()/2),
            QPointF(self.WINGS_STARTING * self.size().width() + self.WINGS_LENGTH * self.size().width(), self.size().height()/2),
            QPointF(self.WINGS_STARTING * self.size().width() + self.WINGS_LENGTH * self.size().width(), self.size().height()/2 + self.WINGS_HEIGHT * self.size().width())
        ]

        # Left wing
        painter.setPen(QPen(self.YELLOW, self.WINGS_WIDTH * self.size().width() + self.WINGS_BORDER_WIDTH*2, Qt.SolidLine))
        painter.drawLine(
            wing_points[0].x(),
            wing_points[0].y(),
            wing_points[1].x(),
            wing_points[1].y(),
        )
        painter.drawLine(
            wing_points[1].x(),
            wing_points[1].y(),
            wing_points[2].x(),
            wing_points[2].y(),
        )
        painter.setPen(QPen(QColor("black"), self.WINGS_WIDTH * self.size().width(), Qt.SolidLine))
        painter.drawLine(
            wing_points[0].x(),
            wing_points[0].y(),
            wing_points[1].x(),
            wing_points[1].y(),
        )
        painter.drawLine(
            wing_points[1].x(),
            wing_points[1].y(),
            wing_points[2].x(),
            wing_points[2].y(),
        )

        # Reflect vertically around center
        for point in wing_points:
            point.setX(-(point.x() - self.size().width() / 2) + self.size().width() / 2)

        # Right wing
        painter.setPen(QPen(self.YELLOW, self.WINGS_WIDTH * self.size().width() + self.WINGS_BORDER_WIDTH*2, Qt.SolidLine))
        painter.drawLine(
            wing_points[0].x(),
            wing_points[0].y(),
            wing_points[1].x(),
            wing_points[1].y(),
        )
        painter.drawLine(
            wing_points[1].x(),
            wing_points[1].y(),
            wing_points[2].x(),
            wing_points[2].y(),
        )
        painter.setPen(QPen(QColor("black"), self.WINGS_WIDTH * self.size().width(), Qt.SolidLine))
        painter.drawLine(
            wing_points[0].x(),
            wing_points[0].y(),
            wing_points[1].x(),
            wing_points[1].y(),
        )
        painter.drawLine(
            wing_points[1].x(),
            wing_points[1].y(),
            wing_points[2].x(),
            wing_points[2].y(),
        )

        # Center Square
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.YELLOW)) # must be even
        self.draw_rect_center(painter, 
                              self.size().width() / 2, 
                              self.size().height() / 2, 
                              self.WINGS_CENTER_SQUARE_SIZE * self.size().width() + self.WINGS_BORDER_WIDTH*2,
                              self.WINGS_CENTER_SQUARE_SIZE * self.size().width() + self.WINGS_BORDER_WIDTH*2)
        painter.setBrush(QBrush(QColor("black")))
        self.draw_rect_center(painter, 
                              self.size().width() / 2, 
                              self.size().height() / 2, 
                              self.WINGS_CENTER_SQUARE_SIZE * self.size().width(),
                              self.WINGS_CENTER_SQUARE_SIZE * self.size().width())

    def draw_background(self, painter, roll, pitch):
        # Set up transformations
        center = QRectF(0, 0, self.size().width(), self.size().height()).center()
        painter.translate(center)
        painter.rotate(-roll)
        painter.translate(-center)

        # Calculate horizon line points
        buffer = self.size().height() * 2 # Just needs to be large enough to cover scale, this is the height of the background in px
        half_height = self.size().height() / 2
        y_offset = self.pitch_deg_to_px(pitch)
        left = -buffer, half_height + y_offset
        right = self.size().width() + buffer, half_height + y_offset

        # Draw sky
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.SKY_COLOR)
        sky_poly = QPolygonF([QPointF(left[0], left[1] - buffer),
                            QPointF(right[0], right[1] - buffer),
                            QPointF(*right),
                            QPointF(*left)])
        painter.drawPolygon(sky_poly)

        # Draw ground
        painter.setBrush(self.GROUND_COLOR)
        ground_poly = QPolygonF([QPointF(left[0], left[1] + buffer),
                                QPointF(right[0], right[1] + buffer),
                                QPointF(*right),
                                QPointF(*left)])
        painter.drawPolygon(ground_poly)

        # Draw horizon line
        painter.setPen(QPen(self.LIGHT_GREY, self.HORIZON_THICKNESS))
        painter.drawLine(QPointF(*left), QPointF(*right))

        painter.resetTransform()

    def clamp(self, value, minval, maxval):
        return sorted((minval, value, maxval))[1]