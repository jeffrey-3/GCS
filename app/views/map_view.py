from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class MapView(QGraphicsView):
    MIN_ZOOM = 1
    MAX_ZOOM = 19
    TILE_SIZE = 500  # Size of tiles in pixels

    clicked = pyqtSignal(tuple)  # Signal emitted when the map is clicked
    key_press_signal = pyqtSignal(QKeyEvent)  # Signal emitted on key press

    def __init__(self):
        super().__init__()
        # Disable scroll bars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a QGraphicsScene to manage graphical items
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Initialize map and plane state variables
        self.accept_radius = 0  # Radius for waypoint acceptance
        self.plane_lat = 0  # Plane's current latitude
        self.plane_lon = 0  # Plane's current longitude
        self.plane_hdg = 0  # Plane's current heading
        self.plane_current_wp = 0  # Index of the current waypoint
        self.map_lat = 0  # Map's center latitude
        self.map_lon = 0  # Map's center longitude
        self.zoom = 16  # Current zoom level
        self.waypoints = []  # List of waypoints
        self.tile_cache = {}  # Cache for loaded tiles to improve performance

    def set_map_position(self, lat, lon):
        """Set the map's center position using latitude and longitude."""
        self.map_lat = lat
        self.map_lon = lon

    def set_plane_position(self, lat, lon, hdg):
        """Set the plane's current position and heading."""
        self.plane_lat = lat
        self.plane_lon = lon
        self.plane_hdg = hdg

    def set_waypoints(self, waypoints):
        """Set the list of waypoints and center the map on the first waypoint if not already centered."""
        self.waypoints = waypoints
        if self.map_lat == 0:  # If the map is not yet centered
            self.set_map_position(waypoints[0].lat, waypoints[0].lon)

    def render(self):
        """Render the map, waypoints, acceptance radius, and plane arrow."""
        self.scene.clear()  # Clear the scene before redrawing
        self.draw_tiles()  # Draw map tiles
        self.draw_accept_radius()  # Draw acceptance radius around waypoints
        self.draw_waypoints()  # Draw waypoints and connecting lines
        self.draw_arrow()  # Draw the plane's arrow

    def wheelEvent(self, event):
        """Ignore wheel events to disable scrolling."""
        event.ignore()

    def keyPressEvent(self, event):
        """Handle key press events for map navigation and zooming."""
        movement_pixels = 100  # Move by 100 pixels per key press
        movement_meters = self.pixels_to_meters(movement_pixels, self.map_lat)

        # Convert movement in meters to degrees
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
        elif event.key() == Qt.Key_Equal:  # Zoom in
            if self.zoom < self.MAX_ZOOM:
                self.zoom += 1
        elif event.key() == Qt.Key_Minus:  # Zoom out
            if self.zoom > self.MIN_ZOOM:
                self.zoom -= 1

        self.render()  # Redraw the map after changes

    def draw_tiles(self):
        """Draw map tiles based on the current zoom level and map center."""
        viewport_width = self.size().width()
        viewport_height = self.size().height()

        # Convert map center to tile coordinates
        center_x, center_y = self.lat_lon_to_tile(self.map_lat, self.map_lon, self.zoom)
        frac_x = center_x - int(center_x)  # Fractional part of tile X
        frac_y = center_y - int(center_y)  # Fractional part of tile Y

        # Calculate the number of tiles needed to cover the viewport
        num_tiles_x = math.ceil(viewport_width / self.TILE_SIZE) + 1
        num_tiles_y = math.ceil(viewport_height / self.TILE_SIZE) + 1

        # Draw tiles around the center tile
        for dx in range(-num_tiles_x // 2, num_tiles_x // 2 + 1):
            for dy in range(-num_tiles_y // 2, num_tiles_y // 2 + 1):
                tile_x = int(center_x) + dx
                tile_y = int(center_y) + dy
                tile_key = (self.zoom, tile_x, tile_y)

                # Load tile from cache or disk
                if tile_key in self.tile_cache:
                    pixmap = self.tile_cache[tile_key]
                else:
                    pixmap = QPixmap(f"tiles/{self.zoom}/{tile_x}/{tile_y}.png")
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(self.TILE_SIZE, self.TILE_SIZE)
                        self.tile_cache[tile_key] = pixmap

                if not pixmap.isNull():
                    # Add the tile to the scene
                    pixmap_item = self.scene.addPixmap(pixmap)
                    pixmap_item.setZValue(-1)  # Ensure tiles are drawn behind other items

                    # Calculate tile position based on fractional offset
                    offset_x = (dx - frac_x) * self.TILE_SIZE + viewport_width // 2
                    offset_y = (dy - frac_y) * self.TILE_SIZE + viewport_height // 2
                    pixmap_item.setPos(offset_x, offset_y)

        # Adjust scene rectangle to match viewport size
        self.setSceneRect(0, 0, viewport_width, viewport_height)

    def draw_waypoints(self):
        """Draw waypoints and connecting lines."""
        if len(self.waypoints) > 0:
            # Convert waypoints to map coordinates
            points = [self.lat_lon_to_map_coords(wp.lat, wp.lon) for wp in self.waypoints]

            # Draw connecting lines
            path = QPainterPath()
            start_point = QPointF(points[0][0], points[0][1])  # Convert tuple to QPointF
            path.moveTo(start_point)
            for point in points[1:]:
                qpoint = QPointF(point[0], point[1])  # Convert tuple to QPointF
                path.lineTo(qpoint)
            polyline_item = QGraphicsPathItem(path)
            polyline_item.setPen(QPen(Qt.magenta, 5))
            self.scene.addItem(polyline_item)

            # Draw waypoint markers
            for i, point in enumerate(points):
                s = "H" if i == 0 else "L" if i == len(self.waypoints) - 1 else str(i + 1)
                radius = 20
                circle = QGraphicsEllipseItem(QRectF(-radius, -radius, 2 * radius, 2 * radius))
                circle.setBrush(QBrush(Qt.black))
                circle.setPen(QPen(Qt.magenta, 5))
                if self.plane_current_wp == i:
                    circle.setBrush(QBrush(QColor(139, 0, 139)))  # Highlight current waypoint
                circle.setPos(QPointF(point[0], point[1]))  # Convert tuple to QPointF
                self.scene.addItem(circle)

                # Add waypoint labels
                text = QGraphicsTextItem(s)
                text.setFont(QFont("Arial", 10))
                text.setDefaultTextColor(Qt.white)
                text.setPos(point[0] - text.boundingRect().width() / 2, point[1] - text.boundingRect().height() / 2)
                self.scene.addItem(text)

    def draw_arrow(self):
        """Draw the plane's arrow at its current position and heading."""
        x, y = self.lat_lon_to_map_coords(self.plane_lat, self.plane_lon)
        arrow_pixmap = QPixmap("app/resources/arrow.png").scaled(50, 50)
        arrow = self.scene.addPixmap(arrow_pixmap)
        arrow.setPos(x - 25, y - 25)  # Center the arrow
        arrow.setTransformOriginPoint(arrow_pixmap.width() / 2, arrow_pixmap.height() / 2)
        arrow.setRotation(self.plane_hdg + 180)  # Rotate the arrow to match heading

    def draw_accept_radius(self):
        """Draw acceptance radius circles around waypoints."""
        if len(self.waypoints) > 0:
            points = [self.lat_lon_to_map_coords(wp.lat, wp.lon) for wp in self.waypoints]
            for i, point in enumerate(points):
                radius = self.meters_to_pixels(self.accept_radius, self.waypoints[i].lat)
                circle = QGraphicsEllipseItem(QRectF(-radius, -radius, 2 * radius, 2 * radius))
                circle.setPen(QPen(Qt.white, 3))
                circle.setPos(QPointF(point[0], point[1]))  # Convert tuple to QPointF
                self.scene.addItem(circle)

    def lat_lon_to_map_coords(self, lat, lon):
        """Convert latitude and longitude to map coordinates (x, y)."""
        tile_x, tile_y = self.lat_lon_to_tile(lat, lon, self.zoom)
        pixel_x = tile_x * self.TILE_SIZE
        pixel_y = tile_y * self.TILE_SIZE

        # Calculate the center tile coordinates in pixels
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
        """Convert meters to pixels based on the current zoom level and latitude."""
        earth_circumference = 40075000  # Earth's circumference in meters
        scale = earth_circumference * math.cos(math.radians(lat)) / (2 ** self.zoom * self.TILE_SIZE)
        return meters / scale

    def pixels_to_meters(self, pixels, lat):
        """Convert pixels to meters based on the current zoom level and latitude."""
        earth_circumference = 40075000
        scale = earth_circumference * math.cos(math.radians(lat)) / (2 ** self.zoom * self.TILE_SIZE)
        return pixels * scale

    def pixel_to_lat_lon(self, x, y):
        """Convert pixel coordinates (x, y) to latitude and longitude."""
        center_tile_x, center_tile_y = self.lat_lon_to_tile(self.map_lat, self.map_lon, self.zoom)
        center_pixel_x = center_tile_x * self.TILE_SIZE
        center_pixel_y = center_tile_y * self.TILE_SIZE

        # Calculate the relative pixel coordinates
        viewport_width = self.size().width()
        viewport_height = self.size().height()
        relative_x = x - viewport_width // 2
        relative_y = y - viewport_height // 2

        # Convert relative pixel coordinates to tile coordinates
        tile_x = (relative_x + center_pixel_x) / self.TILE_SIZE
        tile_y = (relative_y + center_pixel_y) / self.TILE_SIZE

        # Convert tile coordinates to latitude and longitude
        lon = (tile_x / (2 ** self.zoom)) * 360 - 180
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_y / (2 ** self.zoom))))
        lat = math.degrees(lat_rad)

        return lat, lon

    def keyPressEvent(self, event):
        """Handle key press events for map navigation and zooming."""
        # Emit the key press signal
        self.key_press_signal.emit(event)

        # Handle map-specific key events
        movement_pixels = 100  # Move by 100 pixels per key press
        movement_meters = self.pixels_to_meters(movement_pixels, self.map_lat)

        # Convert movement in meters to degrees
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
        elif event.key() == Qt.Key_Equal:  # Zoom in
            if self.zoom < self.MAX_ZOOM:
                self.zoom += 1
        elif event.key() == Qt.Key_Minus:  # Zoom out
            if self.zoom > self.MIN_ZOOM:
                self.zoom -= 1

        self.render()  # Redraw the map after changes