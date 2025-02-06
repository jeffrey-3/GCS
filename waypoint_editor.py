import sys
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
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.clicked.connect(self.addWaypoint)
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.clicked.connect(self.removeWaypoint)
        
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)

        self.createForm()
    
    def createForm(self):
        formGroupBox = QGroupBox("Landing Target")
        layout = QFormLayout()
        self.rwy_lat = QLineEdit("33.021984")
        self.rwy_lon = QLineEdit("-118.590790")
        self.rwy_hdg = QLineEdit("67")
        layout.addRow(QLabel("Latitude"), self.rwy_lat)
        layout.addRow(QLabel("Longitude"), self.rwy_lon)
        layout.addRow(QLabel("Heading"), self.rwy_hdg)
        formGroupBox.setLayout(layout)
        self.layout.addWidget(formGroupBox)

    def loadWaypoints(self, waypoints):
        for lat, lon, alt in waypoints:
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
            if not self.is_float(self.table.item(row, 0).text()) or not self.is_float(self.table.item(row, 1).text()) or not self.is_float(self.table.item(row, 2).text()):
                break
            lat = self.table.item(row, 0).text()
            lon = self.table.item(row, 1).text()
            alt = self.table.item(row, 2).text()
            waypoints.append([float(lat), float(lon), float(alt)])
        return waypoints, float(self.rwy_lat.text()), float(self.rwy_lon.text()), float(self.rwy_hdg.text())

    def is_float(self, element: any) -> bool:
        #If you expect None to be passed:
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False