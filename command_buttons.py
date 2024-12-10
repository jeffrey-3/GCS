from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CommandButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.return_button = QPushButton("Return to Home")
        self.layout.addWidget(self.return_button, 0, 0)

        self.calibrate_button = QPushButton("Calibrate Gyroscopes")
        self.layout.addWidget(self.calibrate_button, 0, 1)