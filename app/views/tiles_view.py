from PyQt5.QtWidgets import *

class TilesView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()

        layout.addRow(QLabel("<h1>Download Map Tiles</h1>"))

        self.top_left_lat_input = QLineEdit("43.879731")
        self.top_left_lon_input = QLineEdit("-79.414462")
        self.bottom_right_lat_input = QLineEdit("43.878084")
        self.bottom_right_lon_input = QLineEdit("-79.411608")
        self.min_zoom_input = QLineEdit("1")
        self.max_zoom_input = QLineEdit("19")

        layout.addRow(QLabel("Top Left Lat"), self.top_left_lat_input)
        layout.addRow(QLabel("Top Left Lon"), self.top_left_lon_input)
        layout.addRow(QLabel("Bottom Right Lat"), self.bottom_right_lat_input)
        layout.addRow(QLabel("Bottom Right Lon"), self.bottom_right_lon_input)
        layout.addRow(QLabel("Min Zoom"), self.min_zoom_input)
        layout.addRow(QLabel("Max Zoom"), self.max_zoom_input)

        self.download_btn = QPushButton("Download Tiles")
        layout.addRow(self.download_btn)

        self.setLayout(layout)