from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from geopy.distance import geodesic
from utils.utils import *
from instruments.map import MapView
from instruments.altitude_profile import AltitudeGraph
from utils.tile_downloader import TileDownloader
import threading
import datetime
import json
from gcs import *


# Squeeze left buttons panel to smallest width




# Store waypoints in planner, not map, map only displays

NO_WAYPOINT_SELECTED = 10000

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

class PlanView(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()
        self.gcs = gcs
        self.waypoints = self.process_flightplan_file("resources/last_flightplan.json")
        self.adding_waypoint = False
        self.selected_waypoint = NO_WAYPOINT_SELECTED

        self.setup_main_layout()
        self.setup_left_panel()
        self.add_tiles_downloader()
        self.setup_right_panel()

        self.addButton.clicked.connect(self.add_btn_press)
        self.deselect_btn.clicked.connect(self.deselect)
        self.removeButton.clicked.connect(self.remove_btn_press)
        self.upload_btn.clicked.connect(self.upload)
        self.editButton.clicked.connect(self.edit_btn_press)
        self.map.clicked_signal.connect(self.clicked)
        self.importButton.clicked.connect(self.import_file)
        self.exportButton.clicked.connect(self.export_file)

        self.update_map()

    def setup_main_layout(self):
        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QGridLayout()

        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 2)

        self.setLayout(self.layout)
    
    def setup_left_panel(self):
        # Title
        self.left_layout.addWidget(QLabel("<h1>Flight Plan</h1>"))

        # Landing stats
        self.landing_label = QLabel("Glideslope Angle:\nLanding Heading:")
        self.landing_label.setStyleSheet("font-size: 12pt;")
        self.left_layout.addWidget(self.landing_label)
        
        buttonLayout = QGridLayout()
        self.left_layout.addLayout(buttonLayout)
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.setStyleSheet("font-size: 12pt;")
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.setStyleSheet("font-size: 12pt;")
        self.editButton = QPushButton("Edit Selected")
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
    
    def setup_right_panel(self):
        self.map = MapView()
        self.map.zoom = 17
        
        self.alt_profile = AltitudeGraph()
        self.alt_profile.set_waypoints(self.map.waypoints)

        self.right_layout.addWidget(self.map)
        self.right_layout.addWidget(self.alt_profile)
        self.right_layout.setRowStretch(0, 3) 
        self.right_layout.setRowStretch(1, 1)

        self.upload_btn = QPushButton("Upload To Vehicle")
        self.upload_btn.setStyleSheet("font-size: 20pt; font-weight: bold;")
        self.left_layout.addWidget(self.upload_btn)
        
    def clicked(self, x, y):
        if self.adding_waypoint:
            lat, lon = self.map.pixel_to_lat_lon(x, y)
            self.map.waypoints.append(Waypoint(lat, lon, self.waypoints[-2].alt))
            self.adding_waypoint = False
            self.deselect()
        else:
            for i in range(len(self.map.waypoints)):
                if i != self.selected_waypoint: # Don't select if already selected
                    wp_x, wp_y = self.map.lat_lon_to_map_coords(self.waypoints[i].lat, self.waypoints[i].lon)
                    if (math.sqrt((x - wp_x)**2 + (y - wp_y)**2) < self.map.waypoint_radius):
                        self.selected_waypoint = i
                        self.update_map()
                        return

            if self.selected_waypoint != NO_WAYPOINT_SELECTED:
                lat, lon = self.map.pixel_to_lat_lon(x, y)
                self.waypoints[self.selected_waypoint].lat = lat
                self.waypoints[self.selected_waypoint].lon = lon
                self.deselect()

    def update_map(self):
        self.map.set_waypoints(self.waypoints)
        self.map.plane_current_wp = self.selected_waypoint
        self.map.render()
        self.alt_profile.set_waypoints(self.waypoints)
        self.calculate_landing_stats(self.map.waypoints, 0)

    def edit_btn_press(self):
        if self.selected_waypoint != NO_WAYPOINT_SELECTED:
            dialog = EditDialog(self.waypoints[self.selected_waypoint].lat,
                                self.waypoints[self.selected_waypoint].lon, 
                                self.waypoints[self.selected_waypoint].alt)
            if dialog.exec_() == QDialog.Accepted:
                lat, lon, alt = dialog.get_values()
                self.waypoints[self.selected_waypoint].lat = lat
                self.waypoints[self.selected_waypoint].lon = lon
                self.waypoints[self.selected_waypoint].alt = alt
                self.deselect()
        else:
            QMessageBox.about(self, "Error", "No waypoint selected")
    
    def upload(self):
        if (self.gcs.send_waypoints(self.waypoints)):
            self.deselect()
            self.save_last_flightplan()
            QMessageBox.about(self, "Status", "Successfully uploaded waypoints")
        else:
            QMessageBox.about(self, "Error", "Upload failed")
    
    def remove_btn_press(self):
        if len(self.waypoints) > 3:
            del self.waypoints[self.selected_waypoint]
            self.deselect()
            self.alt_profile.set_waypoints(self.waypoints)
    
    def deselect(self):
        self.selected_waypoint = NO_WAYPOINT_SELECTED
        self.update_map()
    
    def add_btn_press(self):
        self.adding_waypoint = True
    
    def add_tiles_downloader(self):
        layout = QFormLayout()

        layout.addRow(QLabel("<h1>Download Map Tiles</h1>"))

        self.lat_input = QLineEdit("43.884043")
        self.lon_input = QLineEdit("-79.424526")
        self.size_input = QLineEdit("1000")

        self.lat_input.setStyleSheet("font-size: 12pt;")
        self.lon_input.setStyleSheet("font-size: 12pt;")
        self.size_input.setStyleSheet("font-size: 12pt;")

        self.lat_label = QLabel("Latitude:")
        self.lon_label = QLabel("Longitude:")
        self.size_label = QLabel("Size (m):")

        self.lat_label.setStyleSheet("font-size: 12pt;")
        self.lon_label.setStyleSheet("font-size: 12pt;")
        self.size_label.setStyleSheet("font-size: 12pt;")

        layout.addRow(self.lat_label, self.lat_input)
        layout.addRow(self.lon_label, self.lon_input)
        layout.addRow(self.size_label, self.size_input)

        self.download_btn = QPushButton("Download Tiles")
        self.download_btn.clicked.connect(self.download_tiles)
        self.download_btn.setStyleSheet("font-size: 12pt;")
        layout.addRow(self.download_btn)

        self.left_layout.addLayout(layout)

        self.left_layout.addStretch()
    
    def calculate_landing_stats(self, waypoints, accept_radius):
        position_diff = geodesic((waypoints[-1].lat, waypoints[-1].lon), (waypoints[-2].lat, waypoints[-2].lon)).meters - accept_radius
        alt_diff = waypoints[-2].alt - waypoints[-1].alt
        gs_angle = math.atan(alt_diff / position_diff) * 180 / math.pi
        
        land_hdg = calculate_bearing((waypoints[-2].lat, waypoints[-2].lon), (waypoints[-1].lat, waypoints[-1].lon))

        self.landing_label.setText(f"Glideslope Angle: {gs_angle:.1f}\nLanding Heading: {land_hdg:.1f}")

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
        
    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            waypoints = self.process_flightplan_file(file_path)
            if waypoints:
                self.waypoints = waypoints
                self.update_map()
            else:
                QMessageBox.information(self, "Error", "File format incorrect")
    
    def export_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)")
        if not self.export_flightplan_file(self.waypoints, file_path):
            QMessageBox.information(self, "Error", "Cannot export file. Fields missing.")
    
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
    
    def save_last_flightplan(self):
        json_data = [
            {"lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
            for wp in self.waypoints
        ]

        f = open("resources/last_flightplan.json", "w")
        json.dump(json_data, f, indent=4)

        print("Last flight plan saved")