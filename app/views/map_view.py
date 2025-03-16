from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class MapView(QGraphicsView):
    MIN_ZOOM = 1
    MAX_ZOOM = 19

    # Size of tiles in px
    # Normally is 256px but you can scale up to reduce CPU usage
    TILE_SIZE = 500

    clicked = pyqtSignal(tuple)
    key_press_signal = pyqtSignal(QKeyEvent)

    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.plane_lat = 0
        self.plane_lon = 0
        self.plane_hdg = 0
        self.plane_current_wp = 0
        self.map_lat = 0
        self.map_lon = 0
        self.zoom = 16
        self.waypoints = []
    
    def set_map_position(self, lat, lon):
        self.map_lat = lat
        self.map_lon = lon
    
    def set_plane_position(self, lat, lon, hdg):
        self.plane_lat = lat
        self.plane_lon = lon
        self.plane_hdg = hdg
    
    def set_waypoints(self, waypoints):
        self.waypoints = waypoints

        # If its the first time, pan map to show waypoints
        if self.map_lat == 0:
            self.set_map_position(waypoints[0].lat, waypoints[0].lon)
    
    def render(self):
        self.scene.clear()
        self.draw_tiles()
        self.draw_waypoints()
        self.draw_arrow()
    
    def wheelEvent(self, event):
        # Ignore the wheel event to disable scrolling
        event.ignore()

    def keyPressEvent(self, event):
        movement_pixels = 50  # Move by 50 pixels regardless of zoom

        # Convert movement in pixels to movement in meters
        movement_meters = self.pixels_to_meters(movement_pixels, self.map_lat)

        # Convert movement in meters to movement in degrees (latitude/longitude)
        lat_increment = movement_meters / 111320  # 1° latitude ≈ 111.32 km
        lon_increment = movement_meters / (111320 * math.cos(math.radians(self.map_lat)))  # Adjust for longitude

        if event.key() == Qt.Key_Left:
            self.map_lon -= lon_increment
        elif event.key() == Qt.Key_Right:
            self.map_lon += lon_increment
        elif event.key() == Qt.Key_Up:
            self.map_lat += lat_increment
        elif event.key() == Qt.Key_Down:
            self.map_lat -= lat_increment
        elif event.key() == Qt.Key_Equal:
            if (self.zoom < self.MAX_ZOOM):
                self.zoom += 1
        elif event.key() == Qt.Key_Minus:
            if (self.zoom > self.MIN_ZOOM):
                self.zoom -= 1
        
        self.render()

    def draw_tiles(self):
        viewport_width = self.size().width()
        viewport_height = self.size().height()

        center_x, center_y = self.lat_lon_to_tile(self.map_lat, self.map_lon, self.zoom)

        # Calculate the fractional part of the tile coordinates
        frac_x = center_x - int(center_x)
        frac_y = center_y - int(center_y)

        num_tiles_x = math.ceil(viewport_width / self.TILE_SIZE) + 1
        num_tiles_y = math.ceil(viewport_height / self.TILE_SIZE) + 1

        for dx in range(-num_tiles_x // 2, num_tiles_x // 2 + 1):
            for dy in range(-num_tiles_y // 2, num_tiles_y // 2 + 1):
                tile_x = int(center_x) + dx
                tile_y = int(center_y) + dy

                pixmap = QPixmap(f"tiles/{self.zoom}/{tile_x}/{tile_y}.png")
                
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(self.TILE_SIZE, self.TILE_SIZE)
                    pixmap_item = self.scene.addPixmap(pixmap)
                    pixmap_item.setZValue(-1)
                    
                    # Adjust the position based on the fractional part
                    offset_x = (dx - frac_x) * self.TILE_SIZE + viewport_width // 2
                    offset_y = (dy - frac_y) * self.TILE_SIZE + viewport_height // 2
                    pixmap_item.setPos(offset_x, offset_y)
        
        # Make sure no misalignment when resizing
        self.setSceneRect(0, 0, self.size().width(), self.size().height())
                    
    def draw_waypoints(self):
        if len(self.waypoints) > 0:
            points = []
            for waypoint in self.waypoints:
                x, y = self.lat_lon_to_map_coords(waypoint.lat, waypoint.lon)
                points.append(QPointF(x, y))
            path = QPainterPath()
            path.moveTo(points[0])
            for point in points[1:]:
                path.lineTo(point)
            polyline_item = QGraphicsPathItem(path)
            polyline_item.setPen(QPen(Qt.magenta, 5))
            self.scene.addItem(polyline_item)

            for i, point in enumerate(points):
                s = str(i + 1)
                if i == 0:
                    s = "H"
                elif i == len(self.waypoints) - 1:
                    s = "L"

                radius = 20
                circle = QGraphicsEllipseItem(QRectF(-radius, -radius, 2 * radius, 2 * radius))
                circle.setBrush(QBrush(Qt.black))
                circle.setPen(QPen(Qt.magenta, 5))
                if self.plane_current_wp == i:
                    circle.setBrush(QBrush(QColor(139, 0, 139)))
                circle.setPos(point)
                self.scene.addItem(circle)

                text = QGraphicsTextItem(s)  # Text content (e.g., index + 1)
                text.setFont(QFont("Arial", 10))  # Set font and size
                text.setDefaultTextColor(Qt.white)  # Set text color
                text.setPos(point.x() - text.boundingRect().width() / 2,  # Center the text horizontally
                            point.y() - text.boundingRect().height() / 2)  # Center the text vertically
                self.scene.addItem(text)

    def draw_arrow(self):
        x, y = self.lat_lon_to_map_coords(self.plane_lat, self.plane_lon)
        arrow_pixmap = QPixmap(f"app/resources/arrow.png")
        arrow_pixmap = arrow_pixmap.scaled(50, 50)
        arrow = self.scene.addPixmap(arrow_pixmap)
        arrow.setPos(x - 25, y - 25)
        arrow.setTransformOriginPoint(arrow_pixmap.width() / 2, arrow_pixmap.height() / 2)
        arrow.setRotation(self.plane_hdg + 180)  

    def lat_lon_to_map_coords(self, lat, lon):
        """Convert latitude and longitude to map coordinates (x, y) on the QGraphicsView."""
        # Convert lat/lon to tile coordinates
        tile_x, tile_y = self.lat_lon_to_tile(lat, lon, self.zoom)
        
        # Convert tile coordinates to pixel coordinates
        pixel_x = tile_x * self.TILE_SIZE
        pixel_y = tile_y * self.TILE_SIZE
        
        # Get the center tile coordinates in pixels
        center_tile_x, center_tile_y = self.lat_lon_to_tile(self.map_lat, self.map_lon, self.zoom)
        center_pixel_x = center_tile_x * self.TILE_SIZE
        center_pixel_y = center_tile_y * self.TILE_SIZE
        
        # Calculate the offset from the center of the view
        viewport_width = self.size().width()
        viewport_height = self.size().height()
        
        offset_x = (pixel_x - center_pixel_x) + viewport_width // 2
        offset_y = (pixel_y - center_pixel_y) + viewport_height // 2
        
        return offset_x, offset_y

    def lat_lon_to_tile(self, lat, lon, zoom):
        """Convert latitude, longitude, and zoom level to tile coordinates."""
        lat_rad = math.radians(lat)
        n = 2 ** zoom
        tile_x = n * (lon + 180) / 360
        tile_y = n * (1 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2
        return tile_x, tile_y

    def meters_to_pixels(self, meters, lat):
        """
        Convert meters to pixels on the map at the current zoom level and latitude.
        
        :param meters: Distance in meters.
        :param lat: Latitude at which the distance is measured.
        :return: Distance in pixels.
        """
        # Earth's circumference in meters
        earth_circumference = 40075000  # meters

        # Calculate the scale in meters per pixel
        scale = earth_circumference * math.cos(math.radians(lat)) / (2 ** self.zoom * self.TILE_SIZE)

        # Convert meters to pixels
        pixels = meters / scale

        return pixels

    def pixels_to_meters(self, pixels, lat):
        """
        Convert pixels to meters based on the current zoom level and latitude.

        :param pixels: Distance in pixels.
        :param lat: Latitude at which the distance is measured.
        :return: Distance in meters.
        """
        earth_circumference = 40075000  # Earth's circumference in meters
        scale = earth_circumference * math.cos(math.radians(lat)) / (2 ** self.zoom * self.TILE_SIZE)
        return pixels * scale

    def pixel_to_lat_lon(self, x, y):
        """
        Convert pixel coordinates (x, y) on the QGraphicsView to latitude and longitude.

        :param x: X coordinate in pixels.
        :param y: Y coordinate in pixels.
        :return: Tuple containing latitude and longitude.
        """
        # Get the center tile coordinates in pixels
        center_tile_x, center_tile_y = self.lat_lon_to_tile(self.map_lat, self.map_lon, self.zoom)
        center_pixel_x = center_tile_x * self.TILE_SIZE
        center_pixel_y = center_tile_y * self.TILE_SIZE

        # Calculate the offset from the center of the view
        viewport_width = self.size().width()
        viewport_height = self.size().height()

        # Calculate the pixel coordinates relative to the center tile
        relative_x = x - viewport_width // 2
        relative_y = y - viewport_height // 2

        # Convert the relative pixel coordinates to tile coordinates
        tile_x = (relative_x + center_pixel_x) / self.TILE_SIZE
        tile_y = (relative_y + center_pixel_y) / self.TILE_SIZE

        # Convert tile coordinates to latitude and longitude
        lon = (tile_x / (2 ** self.zoom)) * 360 - 180
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_y / (2 ** self.zoom))))
        lat = math.degrees(lat_rad)

        return lat, lon
    
    def mousePressEvent(self, event):
        # Get the scene position of the mouse click
        scene_pos = self.mapToScene(event.pos())

        # Call the parent class method to ensure normal behavior
        super().mousePressEvent(event)

        self.clicked.emit(self.pixel_to_lat_lon(scene_pos.x(), scene_pos.y()))