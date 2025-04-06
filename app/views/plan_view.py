from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from geopy.distance import geodesic
from app.utils.utils import *
from app.models.config_model import Waypoint

class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(CustomTableWidget, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        event.ignore()

class PlanView(QWidget):
    updated_waypoints = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Flight Plan</h1>"))

        self.landing_label = QLabel("Glideslope Angle:\nLanding Heading:")
        self.landing_label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.landing_label)
        
        # Table setup
        self.table = CustomTableWidget()
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setStyleSheet("font-size: 10pt;")
        self.table.setMinimumHeight(800)
        self.table.setMinimumWidth(800)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Waypoint Type", "Latitude", "Longitude", "Altitude (m)"])
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, 1)  # 1 means stretching mode
        self.layout.addWidget(self.table)
        
        # Buttons for adding and removing rows
        buttonLayout = QGridLayout()
        self.layout.addLayout(buttonLayout)
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.setStyleSheet("font-size: 12pt;")
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.setStyleSheet("font-size: 12pt;")
        self.importButton = QPushButton("Import File")
        self.importButton.setStyleSheet("font-size: 12pt;")
        self.exportButton = QPushButton("Export File")
        self.exportButton.setStyleSheet("font-size: 12pt;")

        self.removeButton.clicked.connect(self.removeWaypoint)
        self.addButton.clicked.connect(self.addWaypoint)
        
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.removeButton, 0, 1)
        buttonLayout.addWidget(self.importButton, 1, 0)
        buttonLayout.addWidget(self.exportButton, 1, 1)

        self.layout.addStretch()

        self.table.cellChanged.connect(self.on_cell_changed)
    
    def get_waypoints(self):
        waypoints = []
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if not self.table.item(row, col):
                    return [], False
            lat = self.table.item(row, 1).text()
            lon = self.table.item(row, 2).text()
            alt = self.table.item(row, 3).text()
            if is_float(lat) and is_float(lon) and is_float(alt):
                waypoints.append(Waypoint(float(lat), float(lon), float(alt)))
            else:
                return [], False
        return waypoints, True

    def addWaypoint(self, lat="", lon="", alt=""):
        rowPosition = self.table.rowCount() - 1 # Insert before last landing waypoint
        self.table.insertRow(rowPosition)
        
        type_item = QTableWidgetItem("WAYPOINT")
        type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)  # Make it read-only
        self.table.setItem(rowPosition, 0, type_item)
        self.table.setItem(rowPosition, 1, QTableWidgetItem(lat))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(lon))
        self.table.setItem(rowPosition, 3, QTableWidgetItem(alt))

    def removeWaypoint(self):
        if self.table.rowCount() > 3 and self.table.currentRow() != 0 and self.table.currentRow() != self.table.rowCount() - 1:
            self.table.removeRow(self.table.currentRow())
            self.on_cell_changed()
    
    def load_waypoints(self, waypoints):
        self.table.setRowCount(0) # Remove all rows
        for row in range(len(waypoints)):
            self.table.insertRow(row)

            if row == 0:
                type = "TAKEOFF"
            elif row == len(waypoints) - 1:
                type = "LAND"
            else:
                type = "WAYPOINT"

            type_item = QTableWidgetItem(type)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)  # Make it read-only
            self.table.setItem(row, 0, type_item)
            self.table.setItem(row, 1, QTableWidgetItem(str(waypoints[row].lat)))
            self.table.setItem(row, 2, QTableWidgetItem(str(waypoints[row].lon)))
            self.table.setItem(row, 3, QTableWidgetItem(str(waypoints[row].alt)))
    
    def clicked(self, pos):
        selectedRows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selectedRows, reverse=True):
            self.table.setItem(row, 1, QTableWidgetItem(str(round(pos[0], 7))))
            self.table.setItem(row, 2, QTableWidgetItem(str(round(pos[1], 7))))
        self.table.clearSelection()

    def on_cell_changed(self):
        waypoints, success = self.get_waypoints()
        if success:
            self.updated_waypoints.emit(waypoints)
        
        self.table.clearSelection()
    
    def clear_table_selection(self):
        self.table.clearSelection()
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.table.clearSelection()
    
    def calculate_landing_stats(self, waypoints, accept_radius):
        if len(waypoints) > 2:
            position_diff = geodesic((waypoints[-1].lat, waypoints[-1].lon), (waypoints[-2].lat, waypoints[-2].lon)).meters - accept_radius
            alt_diff = waypoints[-1].alt - waypoints[-2].alt
            gs_angle = math.atan(alt_diff / position_diff) * 180 / math.pi
            
            land_hdg = calculate_bearing((waypoints[-2].lat, waypoints[-2].lon), (waypoints[-1].lat, waypoints[-1].lon))

            self.landing_label.setText(f"Glideslope Angle: {gs_angle:.1f}\nLanding Heading: {land_hdg:.1f}")
        else:
            self.landing_label.setText("Glideslope Angle:\nLanding Heading:")