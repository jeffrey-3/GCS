from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.utils.data_structures import *
from geopy.distance import geodesic
from app.utils.utils import *

class PlanView(QWidget):
    updated_waypoints = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("<h1>Flight Plan</h1>"))

        self.landing_label = QLabel("Glideslope Angle:\nLanding Heading:")
        self.layout.addWidget(self.landing_label)
        
        # Table setup
        self.table = QTableWidget()
        self.table.setMinimumHeight(600)
        self.table.setMinimumWidth(500)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Waypoint Type", "Latitude", "Longitude", "Altitude (m)"])
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, 1)  # 1 means stretching mode
        self.layout.addWidget(self.table)
        
        # Buttons for adding and removing rows
        buttonLayout = QGridLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.removeButton = QPushButton("Remove Selected")
        self.importButton = QPushButton("Import File")
        self.exportButton = QPushButton("Export File")

        self.removeButton.clicked.connect(self.removeWaypoint)
        self.addButton.clicked.connect(self.addWaypoint)
        
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.removeButton, 0, 1)
        buttonLayout.addWidget(self.importButton, 1, 0)
        buttonLayout.addWidget(self.exportButton, 1, 1)
        
        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)
    
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

    def addWaypoint(self, lat="", lon="", alt=""):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        
        combo = QComboBox()
        combo.addItems(["WAYPOINT", "LANDING"])
        combo.setCurrentIndex(0)
        self.table.setCellWidget(rowPosition, 0, combo)
        self.table.setItem(rowPosition, 1, QTableWidgetItem(lat))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(lon))
        self.table.setItem(rowPosition, 3, QTableWidgetItem(alt))

        # Set custom row headers starting from 0
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem(str(row))
            self.table.setVerticalHeaderItem(row, item)

    def removeWaypoint(self):
        selectedRows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selectedRows, reverse=True):
            self.table.removeRow(row)
        
        self.updated_waypoints.emit(self.getWaypoints())
    
    def load_waypoints(self, waypoints):
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
    
    # pos: (lat, lon)
    def clicked(self, pos):
        selectedRows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selectedRows, reverse=True):
            self.table.setItem(row, 1, QTableWidgetItem(str(round(pos[0], 7))))
            self.table.setItem(row, 2, QTableWidgetItem(str(round(pos[1], 7))))
        self.table.clearSelection()

        print(pos[0], pos[1])

    def on_cell_changed(self):
        print("Changed")

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
                
                land_hdg = calculate_bearing((waypoints[-2].lat, waypoints[-2].lon), (waypoints[-1].lat, waypoints[-1].lon))

                self.landing_label.setText(f"Glideslope Angle: {gs_angle:.1f}\nLanding Heading: {land_hdg:.1f}")
            
            self.updated_waypoints.emit(waypoints)
        else:
            self.landing_label.setText("Glideslope Angle:\nLanding Heading:")