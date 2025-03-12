from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.views.connect_view import ConnectView
from app.controllers.connect_controller import ConnectController

class ConnectPageView(QScrollArea):
    def __init__(self, model):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()

        self.connect_view = ConnectView()
        self.connect_controller = ConnectController(self.connect_view, model)
        self.scroll_layout.addWidget(self.connect_view)

        self.next_btn = QPushButton("Start Mission")
        self.next_btn.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.scroll_layout.addWidget(self.next_btn)

        container = QWidget()
        container.setLayout(self.scroll_layout)
        self.setWidget(container)