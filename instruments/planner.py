from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from geopy.distance import geodesic
from utils.utils import *
from instruments.map import MapView
from instruments.altitude_profile import AltitudeGraph
from utils.tile_downloader import TileDownloader
import threading
import json


# Squeeze left buttons panel to smallest width

# 1. Fix messy add waypoints stuff and 10000
# 2. Add code in upload for uploading waypoints through radio

from dataclasses import dataclass

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float


class PlannerAltitudeProfile(AltitudeGraph):
    def __init__(self):
        super().__init__()
    
    def update_test(self, waypoints):
        self.update(waypoints, 0)

class DownloadProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloading Map Tiles")
        self.setModal(True)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.progress_label = QLabel("Preparing download...")
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        layout.addWidget(self.cancel_button)
        
        self.downloader = None
    
    def start_download(self, downloader, center_lat, center_lon, size_meters, min_zoom, max_zoom):
        self.downloader = downloader
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.finished.connect(self.accept)
        
        # Start download in a separate thread
        download_thread = threading.Thread(
            target=self.downloader.download_all_tiles,
            args=(center_lat, center_lon, size_meters, min_zoom, max_zoom)
        )
        download_thread.start()
    
    def update_progress(self, current, total):
        self.progress_label.setText(f"Downloaded {current} of {total} tiles")
        self.progress_bar.setValue(int((current / total) * 100))
    
    def cancel(self):
        if self.downloader:
            self.downloader.cancel()
        self.reject()

class EditDialog(QDialog):
    def __init__(self, default_lat, default_lon, default_alt):
        super().__init__(None)

        self.setStyleSheet("font-size: 12pt;")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Latitude (deg):"))

        self.lat_input = QDoubleSpinBox()
        self.lat_input.setDecimals(7)
        self.lat_input.setRange(-90, 90)
        self.lat_input.setSingleStep(1E-7)
        self.lat_input.setValue(default_lat)
        self.layout.addWidget(self.lat_input)

        self.layout.addWidget(QLabel("Longitude (deg):"))

        self.lon_input = QDoubleSpinBox()
        self.lon_input.setDecimals(7)
        self.lon_input.setRange(-180, 180)
        self.lon_input.setSingleStep(1E-7)
        self.lon_input.setValue(default_lon)
        self.layout.addWidget(self.lon_input)

        self.layout.addWidget(QLabel("Altitude (m):"))

        self.alt_input = QDoubleSpinBox()
        self.alt_input.setDecimals(2)
        self.alt_input.setRange(-10000, 10000)
        self.alt_input.setSingleStep(1E-2)
        self.alt_input.setValue(default_alt)
        self.layout.addWidget(self.alt_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
    
    def get_values(self):
        return self.lat_input.value(), self.lon_input.value(), self.alt_input.value()

class PlanMap(MapView):
    def __init__(self, radio, view):
        super().__init__()
        self.view = view
        self.radio = radio
        self.last_click_pos = None
        self.adding_waypoint = False
        self.waypoints = []

        self.radio.waypoints_updated.connect(self.set_waypoints)
        self.radio.request_waypoint_signal.connect(self.send_waypoint)
        view.removeButton.clicked.connect(self.remove_btn_press)
        view.addButton.clicked.connect(self.add_btn_press)
        view.upload_btn.clicked.connect(self.upload)
        view.editButton.clicked.connect(self.edit_btn_press)
        view.deselect_btn.clicked.connect(self.deselect)
    
    def send_waypoint(self, index):
        self.radio.send_waypoint(self.waypoints[index])
    
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
                self.view.calculate_landing_stats(self.waypoints, 10)
            else:
                selected = False
                for i in range(len(self.waypoints)):
                    x, y = self.lat_lon_to_map_coords(self.waypoints[i].lat, self.waypoints[i].lon)
                    if (math.sqrt((self.last_click_pos.x() - x)**2 + (self.last_click_pos.y() - y)**2) < self.waypoint_radius):
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
            self.view.alt_profile.update_test(self.waypoints)
    
    def add_btn_press(self):
        self.adding_waypoint = True
    
    def upload(self):
        if (self.radio.upload_waypoints(self.waypoints)):
            self.radio.update_waypoints(self.waypoints)
            self.deselect()
            QMessageBox.about(self, "Status", "Successfully uploaded waypoints")
        else:
            QMessageBox.about(self, "Error", "Upload failed")
    
    def edit_btn_press(self):
        if self.plane_current_wp < len(self.waypoints):
            print(self.waypoints[self.plane_current_wp].alt)
            dialog = EditDialog(self.waypoints[self.plane_current_wp].lat,
                                self.waypoints[self.plane_current_wp].lon, 
                                self.waypoints[self.plane_current_wp].alt)
            if dialog.exec_() == QDialog.Accepted:
                lat, lon, alt = dialog.get_values()
                self.waypoints[self.plane_current_wp].lat = lat
                self.waypoints[self.plane_current_wp].lon = lon
                self.waypoints[self.plane_current_wp].alt = alt
                self.render()
        else:
            QMessageBox.about(self, "Error", "No waypoint selected")
        
    def deselect(self):
        self.plane_current_wp = 10000
        self.render()
        
        
class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(CustomTableWidget, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        event.ignore()

class PlanView(QScrollArea):
    def __init__(self, radio):
        super().__init__()
        self.radio = radio

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.upload_btn = QPushButton("Upload To Vehicle")
        self.upload_btn.setStyleSheet("font-size: 20pt; font-weight: bold;")

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
        self.deselect_btn = QPushButton("Deselect")
        self.deselect_btn.setStyleSheet("font-size: 12pt;")
        
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.removeButton, 0, 1)
        buttonLayout.addWidget(self.editButton, 1, 0)
        buttonLayout.addWidget(self.deselect_btn, 1, 1)
        buttonLayout.addWidget(self.importButton, 2, 0)
        buttonLayout.addWidget(self.exportButton, 2, 1)

        self.add_tiles_downloader()

        self.map = PlanMap(self.radio, self)
        self.map.waypoints = self.process_flightplan_file("resources/last_flightplan.json")
        if len(self.map.waypoints) > 0:
            self.map.map_lat = self.map.waypoints[0].lat
            self.map.map_lon = self.map.waypoints[0].lon
        self.right_layout.addWidget(self.map)
        self.right_layout.setRowStretch(0, 3) 
        
        self.alt_profile = PlannerAltitudeProfile()
        self.right_layout.addWidget(self.alt_profile)
        self.right_layout.setRowStretch(1, 1)

        self.left_layout.addStretch()

        self.left_layout.addWidget(self.upload_btn)

        container = QWidget()
        container.setLayout(self.layout)
        self.setWidget(container)
    
    def add_tiles_downloader(self):
        layout = QFormLayout()

        layout.addRow(QLabel("<h1>Download Map Tiles</h1>"))

        self.lat_input = QLineEdit("43.884043")
        self.lat_input.setStyleSheet("font-size: 12pt;")
        self.lon_input = QLineEdit("-79.424526")
        self.lon_input.setStyleSheet("font-size: 12pt;")
        self.size_input = QLineEdit("1000")
        self.size_input.setStyleSheet("font-size: 12pt;")

        self.lat_label = QLabel("Latitude:")
        self.lat_label.setStyleSheet("font-size: 12pt;")

        self.lon_label = QLabel("Longitude:")
        self.lon_label.setStyleSheet("font-size: 12pt;")

        self.size_label = QLabel("Size (m):")
        self.size_label.setStyleSheet("font-size: 12pt;")

        layout.addRow(self.lat_label, self.lat_input)
        layout.addRow(self.lon_label, self.lon_input)
        layout.addRow(self.size_label, self.size_input)

        self.download_btn = QPushButton("Download Tiles")
        self.download_btn.clicked.connect(self.download_tiles)
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
    
    def download_tiles(self):
        try:
            center_lat = float(self.lat_input.text())
            center_lon = float(self.lon_input.text())
            size_meters = float(self.size_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers for coordinates and size")
            return
        
        downloader = TileDownloader()
        progress_dialog = DownloadProgressDialog(self)
        progress_dialog.start_download(downloader, center_lat, center_lon, size_meters, 
                                    self.map.MIN_ZOOM, self.map.MAX_ZOOM)
        
        if progress_dialog.exec_() == QDialog.Accepted:
            self.map.render()
            QMessageBox.information(self, "Status", "Completed download")
        else:
            QMessageBox.information(self, "Status", "Download canceled")
    
    def process_flightplan_file(self, path):
        try:
            with open(path, 'r') as f:
                json_data = json.load(f)
            
            waypoints = [
                Waypoint(float(wp['lat']), float(wp['lon']), float(wp['alt'])) 
                for wp in json_data
            ]
            return waypoints
        except Exception as e:
            print(f"Error processing flight plan file: {e}")
            return None
        
    def export_flightplan_file(self, waypoints, file_path):
        if waypoints:
            json_data = [
                {"lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
                for wp in waypoints
            ]
            
            if file_path:
                with open(file_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
                    return True
        return False