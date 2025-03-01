import sys
import os
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

# Constants for tile retrieval
TILE_SIZE = 256  # Standard Google Maps tile size
TILE_DIR = "tiles"  # Directory where tiles are stored (e.g., map_tiles/{zoom}/{x}/{y}.png)

def get_tile_path(zoom, x, y):
    """Returns the path of a tile image given zoom, x, y."""
    return os.path.join(TILE_DIR, str(zoom), str(x), f"{y}.png")

class MapView(QGraphicsView):
    from PyQt5.QtGui import QPainter

class MapView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)  # Corrected line
        self.load_tiles(zoom=15, center_x=9150, center_y=11950)

    def load_tiles(self, zoom, center_x, center_y):
        """Loads visible map tiles based on a given center tile."""
        tile_range = 3  # Number of tiles to display in each direction
        for dx in range(-tile_range, tile_range + 1):
            for dy in range(-tile_range, tile_range + 1):
                x, y = center_x + dx, center_y + dy
                tile_path = get_tile_path(zoom, x, y)
                if os.path.exists(tile_path):
                    pixmap = QPixmap(tile_path)
                    item = QGraphicsPixmapItem(pixmap)
                    item.setOffset(x * TILE_SIZE, y * TILE_SIZE)
                    self.scene.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapView()
    viewer.show()
    sys.exit(app.exec_())
