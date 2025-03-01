from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
from data_structures.flight_data_struct import FlightData
import time
import os

class Map(QGraphicsView):
    def __init__(self):
        super().__init__()

        tile_zooms = os.listdir("tiles")
        self.min_zoom = int(tile_zooms[0])
        self.max_zoom = int(tile_zooms[-1])
    
    def setup(self):
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Scroll causing alignment
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.lat = 43.878807
        self.lon = -79.413905
        self.zoom = 16

        self.tile_size = 256

        self.flight_data = FlightData()
        self.waypoints = []

        timer = QTimer(self)
        timer.timeout.connect(self.render)
        timer.start(30)
    
    def wheelEvent(self, event):
        # Ignore the wheel event to disable scrolling
        event.ignore()

    def keyPressEvent(self, event):
        increment = 0.01 / self.zoom
        if event.key() == Qt.Key_Left:
            self.lon = self.lon - increment
        elif event.key() == Qt.Key_Right:
            self.lon = self.lon + increment
        elif event.key() == Qt.Key_Up:
            self.lat = self.lat + increment
        elif event.key() == Qt.Key_Down:
            self.lat = self.lat - increment
        elif event.key() == Qt.Key_Equal:
            if (self.zoom < self.max_zoom):
                self.zoom = self.zoom + 1
        elif event.key() == Qt.Key_Minus:
            if (self.zoom > self.min_zoom):
                self.zoom = self.zoom - 1
    
    def render(self):
        self.scene.clear()

        self.draw_tiles()
        self.draw_waypoints()
        self.draw_arrow()

    def draw_tiles(self):
        viewport_width = self.size().width()
        viewport_height = self.size().height()

        center_x, center_y = self.lat_lon_to_tile(self.lat, self.lon, self.zoom)

        # Calculate the fractional part of the tile coordinates
        frac_x = center_x - int(center_x)
        frac_y = center_y - int(center_y)

        num_tiles_x = math.ceil(viewport_width / self.tile_size) + 1
        num_tiles_y = math.ceil(viewport_height / self.tile_size) + 1

        for dx in range(-num_tiles_x // 2, num_tiles_x // 2 + 1):
            for dy in range(-num_tiles_y // 2, num_tiles_y // 2 + 1):
                tile_x = int(center_x) + dx
                tile_y = int(center_y) + dy

                try:
                    pixmap = QPixmap(f"tiles/{self.zoom}/{tile_x}/{tile_y}.png")
                    pixmap = pixmap.scaled(self.tile_size, self.tile_size)
                    pixmap_item = self.scene.addPixmap(pixmap)
                    pixmap_item.setZValue(-1)
                    
                    # Adjust the position based on the fractional part
                    offset_x = (dx - frac_x) * self.tile_size + viewport_width // 2
                    offset_y = (dy - frac_y) * self.tile_size + viewport_height // 2
                    pixmap_item.setPos(offset_x, offset_y)
                except:
                    print(f"tiles/{self.zoom}/{tile_x}/{tile_y}.png not found")

    def draw_waypoints(self):
        points = []
        for waypoint in self.waypoints:
            x, y = self.lat_lon_to_map_coords(waypoint[0], waypoint[1])
            points.append(QPointF(x, y))
        path = QPainterPath()
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        polyline_item = QGraphicsPathItem(path)
        polyline_item.setPen(QPen(Qt.magenta, 5))
        self.scene.addItem(polyline_item)

    def draw_arrow(self):
        x, y = self.lat_lon_to_map_coords(self.flight_data.lat, self.flight_data.lon)
        arrow_pixmap = QPixmap(f"resources/arrow.png")
        arrow_pixmap = arrow_pixmap.scaled(50, 50)
        arrow = self.scene.addPixmap(arrow_pixmap)
        arrow.setPos(x, y)
        arrow.setTransformOriginPoint(arrow_pixmap.width() / 2, arrow_pixmap.height() / 2)
        arrow.setRotation(self.flight_data.heading + 180)  

    def lat_lon_to_map_coords(self, lat, lon):
        """Convert latitude and longitude to map coordinates (x, y) on the QGraphicsView."""
        # Convert lat/lon to tile coordinates
        tile_x, tile_y = self.lat_lon_to_tile(lat, lon, self.zoom)
        
        # Convert tile coordinates to pixel coordinates
        pixel_x = tile_x * self.tile_size
        pixel_y = tile_y * self.tile_size
        
        # Get the center tile coordinates in pixels
        center_tile_x, center_tile_y = self.lat_lon_to_tile(self.lat, self.lon, self.zoom)
        center_pixel_x = center_tile_x * self.tile_size
        center_pixel_y = center_tile_y * self.tile_size
        
        # Calculate the offset from the center of the view
        viewport_width = self.size().width()
        viewport_height = self.size().height()
        
        offset_x = (pixel_x - center_pixel_x) + viewport_width // 2
        offset_y = (pixel_y - center_pixel_y) + viewport_height // 2
        
        return offset_x, offset_y
    
    def update_data(self, flight_data, waypoints, rwy_lat, rwy_lon, rwy_hdg):
        self.waypoints = waypoints
        self.flight_data = flight_data
        self.lat = flight_data.lat
        self.lon = flight_data.lon
    
    def lat_lon_to_tile(self, lat, lon, zoom):
        """Convert latitude, longitude, and zoom level to tile coordinates."""
        lat_rad = math.radians(lat)
        n = 2 ** zoom
        tile_x = n * (lon + 180) / 360
        tile_y = n * (1 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2
        return tile_x, tile_y