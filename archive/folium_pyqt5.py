# import folium

# # Path to your local tile directory
# local_tile_path = 'tiles/{z}/{x}/{y}.png'

# m = folium.Map(
#     location=[43.8787, -79.41371],  # Lat, long for map center
#     zoom_start=15,
#     tiles=None  # Don't use the default tiles
# )

# folium.TileLayer(
#     tiles=local_tile_path,
#     attr="My Tile Server",
#     name="Offline Tiles"
# ).add_to(m)

# m.save('offline_map.html')



import folium
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

# Path to your local tiles
tiles_path = "tiles/{z}/{x}/{y}.png"

# Create a Folium map
m = folium.Map(location=[43.8787, -79.41371], zoom_start=15, control_scale=True)

# Add the local tile layer to the map
folium.TileLayer(
    tiles=tiles_path,
    attr='Local Tiles',
    name='Local Tiles',
    min_zoom=0,
    max_zoom=18
).add_to(m)

# Render the map as an HTML string
html_string = m.get_root().render()


class MapWindow(QMainWindow):
    def __init__(self, html_string):
        super().__init__()

        # Set up the web view
        self.browser = QWebEngineView()
        self.browser.setHtml(html_string)  # Load the Folium map HTML string directly

        # Set the web view as the central widget
        self.setCentralWidget(self.browser)

        # Set window properties
        self.setWindowTitle("Folium Map in PyQt5")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow(html_string)  # Pass the HTML string to the window
    window.show()
    sys.exit(app.exec_())