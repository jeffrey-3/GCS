from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.params_view import ParamsView
from app.controllers.params_controller import ParamsController

class ParamsPageView(QScrollArea):
    def __init__(self, model):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()

        self.params_view = ParamsView()
        self.params_controller = ParamsController(self.params_view, model)
        self.scroll_layout.addWidget(self.params_view)

        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.scroll_layout.addWidget(self.next_btn)

        container = QWidget()
        container.setLayout(self.scroll_layout)
        self.setWidget(container)