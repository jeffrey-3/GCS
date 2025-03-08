from app.utils.data_structures import *
from PyQt5.QtWidgets import *
from geopy.distance import geodesic
import math
from app.views.tiles_view import TilesView
from app.views.connect_view import ConnectView
from app.views.params_view import ParamsView
from app.views.plan_view import PlanView
from app.models.tiles_model import TilesModel
from app.models.plan_model import PlanModel
from app.models.params_model import ParamsModel
from app.controllers.params_controller import ParamsController
from app.controllers.plan_controller import PlanController
from app.controllers.tiles_controller import TilesController
from app.controllers.connect_controller import ConnectController
from app.utils.utils import *
from PyQt5.QtCore import *

class ConfigView(QWidget):
    def __init__(self):
        super().__init__()

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.create_params_layout()
        self.create_flightplan_layout()
        self.create_tiles_layout()
        self.create_connection_layout()
        self.create_continue_btn()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.container)

        self.scroll.setMinimumWidth(self.container.width() + 100)
        self.setMinimumWidth(self.scroll.width())

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)
        self.setLayout(main_layout)
    
    def create_connection_layout(self):
        self.connect_view = ConnectView()
        self.connect_controller = ConnectController(self.connect_view)
        self.layout.addWidget(self.connect_view)
            
    def create_tiles_layout(self):
        self.tiles_model = TilesModel()
        self.tiles_view = TilesView()
        self.tiles_controller = TilesController(self.tiles_view, self.tiles_model)
        self.layout.addWidget(self.tiles_view)

    def create_flightplan_layout(self):
        self.plan_model = PlanModel()
        self.plan_view = PlanView()
        self.plan_controller = PlanController(self.plan_view, self.plan_model)
        self.layout.addWidget(self.plan_view)
        self.plan_view.table.cellChanged.connect(self.on_cell_changed)
    
    def create_params_layout(self):
        self.params_view = ParamsView()
        self.params_model = ParamsModel()
        self.params_controller = ParamsController(self.params_view, self.params_model)
        self.layout.addWidget(self.params_view)
    
    def create_continue_btn(self):
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setStyleSheet("font-size: 18pt;")
        self.layout.addWidget(self.continue_btn)

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