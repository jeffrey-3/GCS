from lib.tile_downloader.tile_downloader import TileDownloader
from PyQt5.QtWidgets import *

class Tiles(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()

        self.max_lat_input = QLineEdit("43.881725")
        self.min_lat_input = QLineEdit("43.875552")
        self.max_lon_input = QLineEdit("-79.405701")
        self.min_lon_input = QLineEdit("-79.418744")
        self.min_zoom_input = QLineEdit("15")
        self.max_zoom_input = QLineEdit("19")

        layout.addRow(QLabel("Min Latitude"), self.min_lat_input)
        layout.addRow(QLabel("Max Latitude"), self.max_lat_input)
        layout.addRow(QLabel("Min Longitude"), self.min_lon_input)
        layout.addRow(QLabel("Max Longitude"), self.max_lon_input)
        layout.addRow(QLabel("Min Zoom"), self.min_zoom_input)
        layout.addRow(QLabel("Max Zoom"), self.max_zoom_input)

        download_btn = QPushButton("Download Tiles")
        download_btn.clicked.connect(self.download)
        layout.addRow(download_btn)

        self.setLayout(layout)
    
    def download(self):
        min_lat = float(self.min_lat_input.text())
        max_lat = float(self.max_lat_input.text())
        min_lon = float(self.min_lon_input.text())
        max_lon = float(self.max_lon_input.text())
        min_zoom = int(self.min_zoom_input.text())
        max_zoom = int(self.max_zoom_input.text())

        downloader = TileDownloader(threads=10)
        downloader.download_all_tiles(min_lat, max_lat, min_lon, max_lon, min_zoom, max_zoom)

        QMessageBox.information(self, "Status", "Completed download")