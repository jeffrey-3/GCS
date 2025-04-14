from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Calibration(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Calibration</h1>"))

        self.next_btn = QPushButton("Next Position")
        self.next_btn.setStyleSheet("font-size: 12pt;")
        self.next_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.next_btn)

        self.layout.addStretch()