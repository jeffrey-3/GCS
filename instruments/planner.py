from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from geopy.distance import geodesic
from utils.utils import *
from gcs import Waypoint
from instruments.map import MapView
from instruments.altitude_profile import AltitudeGraph

# You still need lat/lon for download tiles because you download tiles at home, and create flight plan on field, so knowledge of waypoints does not exist yet
# Radius from home instead of min/max latlon

class PlanMap(MapView):
    def __init__(self, radio, gcs, view):
        super().__init__(gcs)
        self.last_click_pos = None
        self.adding_waypoint = False
        self.waypoints = gcs.get_waypoints().copy()

        if self.waypoints is not None:
            self.map_lat = self.waypoints[0].lat
            self.map_lon = self.waypoints[0].lon

        self.gcs.waypoints_updated.connect(self.set_waypoints)
        view.removeButton.clicked.connect(self.remove_btn_press)
        view.addButton.clicked.connect(self.add_btn_press)
        view.upload_btn.clicked.connect(self.upload)
    
    def set_waypoints(self, waypoints):
        self.waypoints = waypoints
        if self.map_lat == 0:  # If the map is not yet centered
            self.pan_to_home()
    
    def mousePressEvent(self, event):
        print("Clicked map")
        self.render() # For some reason it messes up pixel coordinates of if not rendered
        """Handle mouse press events to detect clicks on the map."""
        if event.button() == Qt.LeftButton:
            self.last_click_pos = event.pos()

            if self.adding_waypoint:
                lat, lon = self.pixel_to_lat_lon(self.last_click_pos.x(), self.last_click_pos.y())
                self.waypoints.append(Waypoint(lat, lon, self.waypoints[-2].alt))
                self.adding_waypoint = False
                self.plane_current_wp = 10000
                self.render()
            else:
                selected = False
                for i in range(len(self.waypoints)):
                    x, y = self.lat_lon_to_map_coords(self.waypoints[i].lat, self.waypoints[i].lon)
                    if (math.sqrt((self.last_click_pos.x() - x)**2 + (self.last_click_pos.y() - y)**2) < 50):
                        print(i)
                        self.plane_current_wp = i
                        self.render()
                        selected = True
                if not selected:
                    lat, lon = self.pixel_to_lat_lon(self.last_click_pos.x(), self.last_click_pos.y())
                    self.waypoints[self.plane_current_wp] = Waypoint(lat, lon, self.waypoints[self.plane_current_wp].alt)
                    

                    print("Reset map")
                    self.plane_current_wp = 10000
                    self.render()

        super().mousePressEvent(event)
    
    def remove_btn_press(self):
        if len(self.waypoints) > 3:
            del self.waypoints[self.plane_current_wp]
            self.plane_current_wp = 10000
            self.render()
    
    def add_btn_press(self):
        print("add btn press")
        self.adding_waypoint = True
    
    def upload(self):
        print("Upload")
        self.gcs.update_waypoints(self.waypoints)
        
class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(CustomTableWidget, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        event.ignore()

class PlanView(QScrollArea):
    updated_waypoints = pyqtSignal(list)

    def __init__(self, radio, gcs):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.upload_btn = QPushButton("Upload To Vehicle")
        self.upload_btn.setStyleSheet("font-size: 20pt;")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.left_layout = QVBoxLayout()
        self.right_layout = QGridLayout()
        
        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 2)

        self.left_layout.addWidget(QLabel("<h1>Flight Plan</h1>"))

        self.landing_label = QLabel("Glideslope Angle:\nLanding Heading:")
        self.landing_label.setStyleSheet("font-size: 12pt;")
        self.left_layout.addWidget(self.landing_label)
        
        # Buttons for adding and removing rows
        buttonLayout = QGridLayout()
        self.left_layout.addLayout(buttonLayout)
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.setStyleSheet("font-size: 12pt;")
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.setStyleSheet("font-size: 12pt;")
        self.editButton = QPushButton("Edit Selected") # Edit lat/lon/alt
        self.editButton.setStyleSheet("font-size: 12pt;")
        self.importButton = QPushButton("Import File")
        self.importButton.setStyleSheet("font-size: 12pt;")
        self.exportButton = QPushButton("Export File")
        self.exportButton.setStyleSheet("font-size: 12pt;")
        
        buttonLayout.addWidget(self.addButton, 0, 0, 1, 2)
        buttonLayout.addWidget(self.removeButton, 0, 2, 1, 2)
        buttonLayout.addWidget(self.editButton, 0, 4, 1, 2)
        buttonLayout.addWidget(self.importButton, 1, 0, 1, 3)
        buttonLayout.addWidget(self.exportButton, 1, 3, 1, 3)

        self.add_tiles_downloader()

        self.map = PlanMap(radio, gcs, self)
        self.right_layout.addWidget(self.map)
        self.right_layout.setRowStretch(0, 3) 
        
        self.right_layout.addWidget(AltitudeGraph(gcs))
        self.right_layout.setRowStretch(1, 1)

        self.left_layout.addStretch()

        self.left_layout.addWidget(self.upload_btn)

        container = QWidget()
        container.setLayout(self.layout)
        self.setWidget(container)
    
    def add_tiles_downloader(self):
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

        self.bottom_right_lat_label = QLabel("Bottom Right Lat:")
        self.bottom_right_lat_label.setStyleSheet("font-size: 12pt;")

        self.bottom_right_lon_label = QLabel("Bottom Right Lon:")
        self.bottom_right_lon_label.setStyleSheet("font-size: 12pt;")

        self.min_zoom_label = QLabel("Min Zoom:")
        self.min_zoom_label.setStyleSheet("font-size: 12pt;")

        self.max_zoom_label = QLabel("Max Zoom:")
        self.max_zoom_label.setStyleSheet("font-size: 12pt;")

        layout.addRow(self.top_left_lat_label, self.top_left_lat_input)
        layout.addRow(self.top_left_lon_label, self.top_left_lon_input)
        layout.addRow(self.bottom_right_lat_label, self.bottom_right_lat_input)
        layout.addRow(self.bottom_right_lon_label, self.bottom_right_lon_input)
        layout.addRow(self.min_zoom_label, self.min_zoom_input)
        layout.addRow(self.max_zoom_label, self.max_zoom_input)

        self.download_btn = QPushButton("Download Tiles")
        self.download_btn.setStyleSheet("font-size: 12pt;")
        layout.addRow(self.download_btn)

        self.left_layout.addLayout(layout)
    
    def calculate_landing_stats(self, waypoints, accept_radius):
        if len(waypoints) > 2:
            position_diff = geodesic((waypoints[-1].lat, waypoints[-1].lon), (waypoints[-2].lat, waypoints[-2].lon)).meters - accept_radius
            alt_diff = waypoints[-1].alt - waypoints[-2].alt
            gs_angle = math.atan(alt_diff / position_diff) * 180 / math.pi
            
            land_hdg = calculate_bearing((waypoints[-2].lat, waypoints[-2].lon), (waypoints[-1].lat, waypoints[-1].lon))

            self.landing_label.setText(f"Glideslope Angle: {gs_angle:.1f}\nLanding Heading: {land_hdg:.1f}")
        else:
            self.landing_label.setText("Glideslope Angle:\nLanding Heading:")