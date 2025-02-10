import json
import datetime
from PyQt5.QtWidgets import *

class WaypointEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Latitude", "Longitude", "Altitude"])
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, 1)  # 1 means stretching mode
        self.layout.addWidget(self.table)
        
        # Buttons for adding and removing rows
        buttonLayout = QGridLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.clicked.connect(self.addWaypoint)
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.clicked.connect(self.removeWaypoint)
        self.importButton = QPushButton("Import File")
        self.importButton.clicked.connect(self.load_file)
        self.exportButton = QPushButton("Export File")
        self.exportButton.clicked.connect(self.save_file)
        
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.removeButton, 0, 1)
        buttonLayout.addWidget(self.importButton, 1, 0)
        buttonLayout.addWidget(self.exportButton, 1, 1)
        
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)

        self.createForm()
    
    def save_file(self):
        waypoints, rwy_lat, rwy_lon, rwy_hdg = self.getWaypoints()
        json_data = {
            "waypoints": [
                {"lat": wp[0], "lon": wp[1], "alt": wp[2]} for wp in waypoints
            ],
            "landing": {
                "lat": rwy_lat,
                "lon": rwy_lon,
                "hdg": rwy_hdg
            }
        }

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", 'plan_{date:%Y_%m_%d_%H_%M_%S}.json'.format(date=datetime.datetime.now()), "JSON Files (*.json)", options=options)
        
        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(json_data, json_file, indent=4)

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_name:
            f = open(file_name, 'r')

            json_data = json.load(f)
            rwy_data = json_data['landing']

            self.rwy_lat.setText(str(rwy_data['lat']))
            self.rwy_lon.setText(str(rwy_data['lon']))
            self.rwy_hdg.setText(str(rwy_data['hdg']))

            waypoints_data = json_data['waypoints']
            print(waypoints_data)

            self.table.setRowCount(0) # Remove all rows
            for row in range(len(waypoints_data)):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(waypoints_data[row]['lat'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(waypoints_data[row]['lon'])))
                self.table.setItem(row, 2, QTableWidgetItem(str(waypoints_data[row]['alt'])))
    
    def createForm(self):
        formGroupBox = QGroupBox("Landing Target")
        layout = QFormLayout()

        self.rwy_lat = QLineEdit()
        self.rwy_lon = QLineEdit()
        self.rwy_hdg = QLineEdit()

        layout.addRow(QLabel("Latitude"), self.rwy_lat)
        layout.addRow(QLabel("Longitude"), self.rwy_lon)
        layout.addRow(QLabel("Heading"), self.rwy_hdg)
        
        formGroupBox.setLayout(layout)
        self.layout.addWidget(formGroupBox)

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
            if not self.is_float(self.table.item(row, 0).text()) or not self.is_float(self.table.item(row, 1).text()) or not self.is_float(self.table.item(row, 2).text()):
                return
            lat = self.table.item(row, 0).text()
            lon = self.table.item(row, 1).text()
            alt = self.table.item(row, 2).text()
            waypoints.append([float(lat), float(lon), float(alt)])

        return waypoints

    def get_land_target(self):
        if self.is_float(self.rwy_lat.text()) and self.is_float(self.rwy_lon.text()) and self.is_float(self.rwy_hdg.text()):
            return float(self.rwy_lat.text()), float(self.rwy_lon.text()), float(self.rwy_hdg.text())

    def is_float(self, element: any) -> bool:
        #If you expect None to be passed:
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False