from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from instruments.planner import PlanView
from instruments.params import ParamsView
from instruments.calibration import Calibration
from instruments.connect import ConnectView
from instruments.flight_display import FlightDisplay
from utils.utils import *
from gcs import GCS
import unreal_stylesheet

# Lines on navigastion display add black outline so theres two colours 

# CAlib ui

# QUICK VIEW IS WHATS CAUSING THE LAG
# WHEN I GO TO RAW VIEW THERES NO MORE LAG

# NUMBER ONE PRIORITY GETTING RADIO TO WORK

# Slow performance on higher res screen

# Spend time on bigger tasks first not this nickpick

# Laggy after running for long time because path

# In the case it overshoots runway on approach, it will keep extrapolating the altitude downwards from glideslope so its fine

# You don't need deselect button if you have drag and drop
# When you click outside waypoint it deselects it, when you drag and drop it moves it

# Maybe implement the rate TECS so it only targets descent rate instead of alt. That way avoids the big dip down if it doesn't follow glidesope.

# What happens if GCS accidentally closed? A button to load params from vehicle in that case, actually no, as soon as you press connect button it automatically requests from vehicle

# BUTTONS INSTEAD OF ARROW KEYS FOR PANNING MAP BECAUSE TOO FINICKY
# - actually its fine, just remove form in download map tiles 
# - or use buttons for planner, but no buttons for flight display (because only zoom needed, no pan)
# - nah too finicky, buttons for everything

# EKF uses NED internally but publishes north east and altitude (up)
# Global frame is lat/lon/alt
# Nevermind, if you use NED for everything instead of both NED and alt then you don't have to worry about it

# Put connect button on top bar not its own page so I can see flight display while connecting. If I go to connect page, I can't see flight display anymore.

# Don't calculate landing stats if parameters not loaded (bnecause dont have acc rad yet) and add indicator that params not loaded

# Indicator for adding waypoint

# Force takeoff waypoint to 0 alt

# Like mission planner, in quick view make text smaller if its more digits so it fits in 3x3 grid evenly

# Quick view fix to 4 characters so it doesnt go smaller than it can
# Actually in reality it wont jitter that much...

# In flight display when not clicked on map the arrow keys don't work

# Move state view to quick

# 1. Figure out how to make aplink python lib cleaner
# 4. rename everything

# Top bar using qhboxlayout with buttons

# PFD red areas

# exe

# Logger

# modern theme

# Maybe interpolate speed setpoints so it doesn't pitch up voilently immediately

# Draw triangle instead of image and then you can use white outline

# Log file replay

# Scale raw view with width because if its too small

# Pyqt6 has dark mode

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gcs = GCS()

        self.setWindowTitle("UAV Ground Control")

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)
        
        main_tabs = QTabWidget()
        main_tabs.setFocusPolicy(Qt.NoFocus)
        main_tabs.setFont(self.tabs_font)
        main_tabs.addTab(FlightDisplay(self.gcs), "Flight")
        main_tabs.addTab(PlanView(self.gcs), "Waypoints")
        main_tabs.addTab(ParamsView(self.gcs), "Parameters")
        main_tabs.addTab(Calibration(self.gcs), "Calibration")
        main_tabs.addTab(QWidget(), "Parse Logs")
        main_tabs.addTab(ConnectView(self.gcs), "Connect")
        
        self.setCentralWidget(main_tabs)
        
if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication([])

    unreal_stylesheet.setup()
        
    main_window = MainView()
    # main_window.showFullScreen()
    main_window.show()

    app.exec()