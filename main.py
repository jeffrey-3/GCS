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
from gcs import GCS

# NUMBER ONE PRIORITY GETTING RADIO TO WORK

# Slow performance on higher res screen

# Spend time on bigger tasks first not this nickpick

# Laggy after running for long time because path

# Look at alt setpoint for flare instead of altitude?

# In the case it overshoots runway on approach, it will keep extrapolating the altitude downwards from glideslope so its fine

# You don't need deselect button if you have drag and drop
# When you click outside waypoint it deselects it, when you drag and drop it moves it

# What happens if GCS accidentally closed? A button to load params from vehicle in that case, actually no, as soon as you press connect button it automatically requests from vehicle

# Altitude graph cut off at the bottom

# Only scale based on width, not height, because height is just to make everything fit pretend lik height is fixed

# BUTTONS INSTEAD OF ARROW KEYS FOR PANNING MAP BECAUSE TOO FINICKY
# - actually its fine, just remove form in download map tiles 
# - or use buttons for planner, but no buttons for flight display (because only zoom needed, no pan)
# - nah too finicky, buttons for everything

# EKF uses NED internally but publishes north east and altitude (up)
# Global frame is lat/lon/alt
# Nevermind, if you use NED for everything instead of both NED and alt then you don't have to worry about it

# circle to show acceptance radius 

# Put connect button on top bar not its own page so I can see flight display while connecting. If I go to connect page, I can't see flight display anymore.

# Vsplitter for altitude profile, on larger screens can be smaller

# Force takeoff waypoint to 0 alt

# Quick view fix to 4 characters so it doesnt go smaller than it can

# Move state view to quick

# 1. Figure out how to make aplink python lib cleaner
# 2. add more signals
# 4. rename everything

# Top bar using qhboxlayout with buttons

# PFD red areas

# exe

# Logger

# point on altitude graph that shows where plane is, calculate based on cross track error

# modern theme

# Maybe interpolate speed setpoints so it doesn't pitch up voilently immediately

# Flight software look at velocity estimate to see if converged (actually doesn't matter, user can just make sure before starting)

# Log file replay

# Scale state, raw, and quick view text size with width

# Pyqt6 has dark mode

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gcs = GCS()

        self.setWindowTitle("UAV Ground Control")

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)
        
        main_tabs = QTabWidget()
        main_tabs.setFont(self.tabs_font)
        main_tabs.addTab(FlightDisplay(self.gcs), "Flight")
        main_tabs.addTab(PlanView(self.gcs), "Waypoints")
        main_tabs.addTab(ParamsView(self.gcs), "Parameters")
        main_tabs.addTab(Calibration(), "Calibration")
        main_tabs.addTab(QWidget(), "Parse Logs")
        main_tabs.addTab(ConnectView(self.gcs), "Connect")
        
        self.setCentralWidget(main_tabs)
        
if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication([])

    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    QApplication.setPalette(dark_palette)
    
    # qdarktheme.setup_theme(corner_shape="sharp")
    # qdarktheme.load_palette() # This causes bottom of altitude profile to be cut off, need to fix

    main_window = MainView()
    # main_window.showFullScreen()
    # main_window.showMaximized()
    main_window.show()

    app.exec()