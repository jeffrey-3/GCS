from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
from instruments.planner import PlanView
from instruments.params import ParamsView
from instruments.calibration import Calibration
from instruments.connect import ConnectView
from instruments.flight_display import FlightDisplay
from utils.utils import *
from radio import Radio

# Scale font size based on window size

# Add more signals to radio and more aplink messages
# Then you can test the other instruments like raw

# 1. Figure out how to make aplink python lib cleaner
# 2. add more signals
# 4. rename everything

# Top bar using qhboxlayout with buttons

# Clickable map is simpler code wise becuase you can just store waypoints in a single module, write this in GCS docs
# Buttons and planner both in same planner.py file so its easy to transfer between

# PFD red areas

# PFD pitch scale numbers

# exe

# Path nav dipaly trajcetory

# modern theme

# if you change first waypoint, then center lat/lon will be off.... maybe use EKF center is better
# Just prevent changing waypoint before the current waypoint in flight?
# But what happens if you load waypoints, ekf initialize, then you change takeoff point agian before flight, it will take time to converge...
# Or just re-converge every time you load new waypoints 
# Or send lat/lon instead of float for position estimate

# Flight software look at velocity estimate to see if converged (actually doesn't matter, user can just make sure before starting)


class MainView(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.radio = Radio()

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)
        
        self.setWindowTitle("UAV Ground Control")
        
        main_tabs = QTabWidget()
        main_tabs.setFont(self.tabs_font)
        main_tabs.addTab(FlightDisplay(self.radio), "Flight")
        main_tabs.addTab(PlanView(self.radio), "Waypoints")
        main_tabs.addTab(ParamsView(self.radio), "Parameters")
        main_tabs.addTab(Calibration(), "Calibration")
        main_tabs.addTab(QWidget(), "Download Logs")
        main_tabs.addTab(ConnectView(self.radio), "Connect")
        
        self.setCentralWidget(main_tabs)
        
if __name__ == "__main__":
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication([])

    qdarktheme.setup_theme(corner_shape="sharp")
    qdarktheme.load_palette()

    main_window = MainView(app)
    main_window.show()
    app.exec()