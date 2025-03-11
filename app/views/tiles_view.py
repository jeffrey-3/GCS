from PyQt5.QtWidgets import *

class TilesView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()

        layout.addRow(QLabel("<h1>Download Map Tiles</h1>"))

        self.top_left_lat_input = QLineEdit("43.884043")
        self.top_left_lat_input.setStyleSheet("font-size: 12pt;")
        self.top_left_lon_input = QLineEdit("-79.424526")
        self.top_left_lon_input.setStyleSheet("font-size: 12pt;")
        self.bottom_right_lat_input = QLineEdit("43.874797")
        self.bottom_right_lat_input.setStyleSheet("font-size: 12pt;")
        self.bottom_right_lon_input = QLineEdit("-79.404941")
        self.bottom_right_lon_input.setStyleSheet("font-size: 12pt;")
        self.min_zoom_input = QLineEdit("1")
        self.min_zoom_input.setStyleSheet("font-size: 12pt;")
        self.max_zoom_input = QLineEdit("19")
        self.max_zoom_input.setStyleSheet("font-size: 12pt;")

        self.top_left_lat_label = QLabel("Top Left Lat:")
        self.top_left_lat_label.setStyleSheet("font-size: 12pt;")

        self.top_left_lon_label = QLabel("Top Left Lon:")
        self.top_left_lon_label.setStyleSheet("font-size: 12pt;")

        self.bottom_right_lat_label = QLabel("Bottom Right Lat")
        self.bottom_right_lat_label.setStyleSheet("font-size: 12pt;")

        self.bottom_right_lon_label = QLabel("Bottom Right Lon")
        self.bottom_right_lon_label.setStyleSheet("font-size: 12pt;")

        self.min_zoom_label = QLabel("Min Zoom")
        self.min_zoom_label.setStyleSheet("font-size: 12pt;")

        self.max_zoom_label = QLabel("Max Zoom")
        self.max_zoom_label.setStyleSheet("font-size: 12pt;")

        layout.addRow(self.top_left_lat_label, self.top_left_lat_input)
        layout.addRow(self.top_left_lon_label, self.top_left_lon_input)
        layout.addRow(self.bottom_right_lat_label, self.bottom_right_lat_input)
        layout.addRow(self.bottom_right_lon_label, self.bottom_right_lon_input)
        layout.addRow(self.min_zoom_label, self.min_zoom_input)
        layout.addRow(self.max_zoom_label, self.max_zoom_input)

        self.download_btn = QPushButton("Download Tiles")
        layout.addRow(self.download_btn)

        self.setLayout(layout)