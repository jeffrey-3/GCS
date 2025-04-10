from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
from instruments.planner import PlanView
from instruments.params import ParamsView
from instruments.connect import ConnectView
from instruments.flight_display import FlightDisplay
from utils.utils import *
from gcs import GCS
from communication.radio import Radio

# Add more signals to radio and more aplink messages
# Then you can test the other instruments like raw

# 2. Get it working with preflight sidebar removed
# 3. Test qpainter writing to QWidget instead of canvas
# 4. rename everything

# Top bar using qhboxlayout with buttons

# Clickable map is simpler code wise becuase you can just store waypoints in a single module
# Buttons and planner both in same planner.py file so its easy to transfer between

# modern theme
# Flight view

class MainView(QMainWindow):
    def __init__(self, app, radio, gcs):
        super().__init__()
        self.app = app
        self.radio = radio
        self.gcs = gcs

        self.tabs_font = QFont()
        self.tabs_font.setPointSize(12)
        
        self.setWindowTitle("UAV Ground Control")
        
        main_tabs = QTabWidget()
        main_tabs.setFont(self.tabs_font)
        main_tabs.addTab(FlightDisplay(self.radio, self.gcs), "Flight")
        main_tabs.addTab(PlanView(self.radio, self.gcs), "Waypoints")
        main_tabs.addTab(ParamsView(), "Parameters")
        main_tabs.addTab(QWidget(), "Calibration")
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
    gcs = GCS()
    radio = Radio()
    main_window = MainView(app, radio, gcs)
    main_window.show()
    app.exec()