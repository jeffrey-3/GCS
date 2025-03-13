from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.tiles_view import TilesView
from app.views.plan_view import PlanView
from app.controllers.plan_controller import PlanController
from app.controllers.tiles_controller import TilesController

class PlanPageView(QScrollArea):
    def __init__(self, model):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()

        self.plan_view = PlanView()
        self.plan_controller = PlanController(self.plan_view, model)
        self.scroll_layout.addWidget(self.plan_view)

        self.tiles_view = TilesView()
        self.tiles_controller = TilesController(self.tiles_view, model)
        self.scroll_layout.addWidget(self.tiles_view)

        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.next_btn.clicked.connect(self.plan_view.clear_table_selection)
        self.scroll_layout.addWidget(self.next_btn)

        container = QWidget()
        container.setLayout(self.scroll_layout)
        self.setWidget(container)