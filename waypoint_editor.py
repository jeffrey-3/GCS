import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout
)

class WaypointEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setDefaultWaypoints()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Latitude", "Longitude", "Altitude"])
        self.table.horizontalHeader().setStretchLastSection(True)
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, 1)  # 1 means stretching mode
        layout.addWidget(self.table)
        
        # Buttons for adding and removing rows
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.clicked.connect(self.addWaypoint)
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.clicked.connect(self.removeWaypoint)
        
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def setDefaultWaypoints(self):
        default_waypoints = [
            (37.7749, -122.4194, 30),
            (34.0522, -118.2437, 50),
            (40.7128, -74.0060, 100)
        ]
        
        for lat, lon, alt in default_waypoints:
            self.addWaypoint(str(lat), str(lon), str(alt))

    def addWaypoint(self, lat="", lon="", alt=""):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        
        # Making cells editable
        self.table.setItem(rowPosition, 0, QTableWidgetItem(lat))
        self.table.setItem(rowPosition, 1, QTableWidgetItem(lon))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(alt))

    def removeWaypoint(self):
        selectedRows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selectedRows, reverse=True):
            self.table.removeRow(row)
    
    def getWaypoints(self):
        waypoints = []
        for row in range(self.table.rowCount()):
            lat = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            lon = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            alt = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            waypoints.append((float(lat), float(lon), float(alt)))
        return waypoints