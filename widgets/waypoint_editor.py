import json
import datetime
from lib.data_structures.data_structures import *
from PyQt5.QtWidgets import *
from geopy.distance import geodesic
import math
from widgets.tiles import Tiles
from lib.utils.utils import *
import serial.tools.list_ports
from PyQt5.QtCore import *
import serial

class WaypointEditor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.create_params_layout()
        self.create_flightplan_layout()
        self.create_tiles_layout()
        self.create_connection_layout()
        
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setStyleSheet("font-size: 18pt;")
        self.layout.addWidget(self.continue_btn)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.container)

        self.scroll.setMinimumWidth(self.container.width() + 100)
        self.setMinimumWidth(self.scroll.width())

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)
        self.setLayout(main_layout)
    
    def create_connection_layout(self):
        self.layout.addWidget(QLabel("<h1>Connection</h1>"))

        # COM Port Selection
        self.com_port_label = QLabel("Select COM Port:")
        self.layout.addWidget(self.com_port_label)

        self.com_port_dropdown = QComboBox()
        self.layout.addWidget(self.com_port_dropdown)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh COM Ports")
        self.refresh_button.clicked.connect(self.refresh_com_ports)
        self.layout.addWidget(self.refresh_button)

        # Initialize COM ports
        self.refresh_com_ports()
    
    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_dropdown.addItem(port.device)
        self.com_port_dropdown.addItem("Testing")
            
    def create_tiles_layout(self):
        self.layout.addWidget(QLabel("<h1>Download Map Tiles</h1>"))
        self.tiles = Tiles()
        self.layout.addWidget(self.tiles)

    def create_flightplan_layout(self):
        self.layout.addWidget(QLabel("<h1>Flight Plan</h1>"))

        self.landing_label = QLabel("Glideslope Angle:\nLanding Heading:")
        self.layout.addWidget(self.landing_label)
        
        # Table setup
        self.table = QTableWidget()
        self.table.setMinimumHeight(600)
        self.table.setMinimumWidth(1000)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Waypoint Type", "Latitude", "Longitude", "Altitude (m)"])
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, 1)  # 1 means stretching mode
        self.layout.addWidget(self.table)
        self.table.cellChanged.connect(self.on_cell_changed)
        
        # Buttons for adding and removing rows
        buttonLayout = QGridLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.clicked.connect(self.addWaypoint)
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.clicked.connect(self.removeWaypoint)
        self.importButton = QPushButton("Import File")
        self.exportButton = QPushButton("Export File")
        self.exportButton.clicked.connect(self.save_file)
        
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.removeButton, 0, 1)
        buttonLayout.addWidget(self.importButton, 1, 0)
        buttonLayout.addWidget(self.exportButton, 1, 1)
        
        self.layout.addLayout(buttonLayout)
    
    def create_params_layout(self):
        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))
        self.params_file_label = QLineEdit()
        self.params_file_label.setFixedWidth(600)
        self.params_btn = QPushButton("Import Parameters")
        formlayout = QFormLayout()
        formlayout.addRow(self.params_file_label, self.params_btn)
        self.layout.addLayout(formlayout)

    def on_cell_changed(self):
        waypoints = self.getWaypoints()
        if waypoints:
            land_wp_exists = False
            for waypoint in waypoints:
                if waypoint.type == WaypointType.LAND:
                    land_wp_exists = True

            if land_wp_exists:
                position_diff = geodesic((waypoints[-1].lat, waypoints[-1].lon), (waypoints[-2].lat, waypoints[-2].lon)).meters
                alt_diff = waypoints[-1].alt - waypoints[-2].alt
                gs_angle = math.atan(alt_diff / position_diff) * 180 / math.pi
                
                land_hdg = calculate_bearing((waypoints[-1].lat, waypoints[-1].lon), (waypoints[-2].lat, waypoints[-2].lon))

                self.landing_label.setText(f"Glideslope Angle: {gs_angle:.1f}\nLanding Heading: {land_hdg:.1f}")
        else:
            self.landing_label.setText("Glideslope Angle:\nLanding Heading:")
    
    def save_file(self):
        waypoints = self.getWaypoints()
        if waypoints:
            json_data = [
                {"type": wp.type, "lat": wp.lat, "lon": wp.lon, "alt": wp.alt} 
                for wp in waypoints
            ]
            
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
            if file_path:
                with open(file_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
        else:
            QMessageBox.information(self, "Error", "Cannot export file. Fields missing.")

    def load_flightplan(self, waypoints):
        self.table.setRowCount(0) # Remove all rows
        for row in range(len(waypoints)):
            self.table.insertRow(row)

            combo = QComboBox()
            combo.addItems(["WAYPOINT", "LANDING"])
            if waypoints[row].type == WaypointType.WAYPOINT:
                combo.setCurrentIndex(0)
            if waypoints[row].type == WaypointType.LAND:
                combo.setCurrentIndex(1)

            self.table.setCellWidget(row, 0, combo)
            self.table.setItem(row, 1, QTableWidgetItem(str(waypoints[row].lat)))
            self.table.setItem(row, 2, QTableWidgetItem(str(waypoints[row].lon)))
            self.table.setItem(row, 3, QTableWidgetItem(str(waypoints[row].alt)))

    def addWaypoint(self, lat="", lon="", alt=""):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        
        # Making cells editable
        self.table.setItem(rowPosition, 0, QTableWidgetItem(lat))
        self.table.setItem(rowPosition, 1, QTableWidgetItem(lon))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(alt))

        # Set custom row headers starting from 0
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem(str(row))
            self.table.setVerticalHeaderItem(row, item)

    def removeWaypoint(self):
        selectedRows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selectedRows, reverse=True):
            self.table.removeRow(row)

    def getWaypoints(self):
        waypoints = []
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if not self.table.item(row, col) and not self.table.cellWidget(row, col):
                    return
            type = self.table.cellWidget(row, 0).currentIndex()
            lat = self.table.item(row, 1).text()
            lon = self.table.item(row, 2).text()
            alt = self.table.item(row, 3).text()
            waypoints.append(Waypoint(WaypointType(type), float(lat), float(lon), float(alt)))
        return waypoints

    def is_float(self, element: any) -> bool:
        #If you expect None to be passed:
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False