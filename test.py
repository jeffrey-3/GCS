import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QTabWidget
)

class WaypointEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setDefaultWaypoints()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.waypointTab = QWidget()
        self.tabs.addTab(self.waypointTab, "Waypoints")
        
        # Waypoint Table Layout
        tabLayout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Latitude", "Longitude", "Altitude"])
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.setSizePolicy(self.table.sizePolicy().Expanding, self.table.sizePolicy().Expanding)
        tabLayout.addWidget(self.table)
        
        # Buttons for adding and removing rows
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Waypoint")
        self.addButton.clicked.connect(self.addWaypoint)
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.clicked.connect(self.removeWaypoint)
        self.printButton = QPushButton("Print Waypoints")
        self.printButton.clicked.connect(self.printWaypoints)
        
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        buttonLayout.addWidget(self.printButton)
        
        tabLayout.addLayout(buttonLayout)
        self.waypointTab.setLayout(tabLayout)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def setDefaultWaypoints(self):
        default_waypoints = [
            ("37.7749", "-122.4194", "30"),
            ("34.0522", "-118.2437", "50"),
            ("40.7128", "-74.0060", "100")
        ]
        
        for lat, lon, alt in default_waypoints:
            self.addWaypoint(lat, lon, alt)

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
    
    def printWaypoints(self):
        waypoints = []
        for row in range(self.table.rowCount()):
            lat = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            lon = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            alt = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            waypoints.append((lat, lon, alt))
        print("Waypoints:", waypoints)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = WaypointEditor()
    editor.setWindowTitle("Waypoint Editor")
    editor.resize(600, 400)
    editor.show()
    sys.exit(app.exec_())
