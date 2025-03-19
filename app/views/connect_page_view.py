from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.connect_view import ConnectView
from app.controllers.connect_controller import ConnectController

class ConnectPageView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.create_scroll_area()
        self.layout.addWidget(self.scroll_area)

        self.next_btn = QPushButton("Start Mission")
        self.next_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.layout.addWidget(self.next_btn)
    
    def create_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()

        self.connect_view = ConnectView()
        self.connect_controller = ConnectController(self.connect_view, self.model)
        self.scroll_layout.addWidget(self.connect_view)

        container = QWidget()
        container.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(container)