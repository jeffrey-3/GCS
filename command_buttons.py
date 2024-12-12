from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CommandButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.altitude_input = QLineEdit("Altitude")
        self.layout.addWidget(self.altitude_input, 0, 0)

        self.heading_input = QLineEdit("Heading")
        self.layout.addWidget(self.heading_input, 0, 1)

        self.return_button = QPushButton("Return to Home")
        self.layout.addWidget(self.return_button, 1, 0)

        self.calibrate_button = QPushButton("Calibrate Gyroscopes")
        self.layout.addWidget(self.calibrate_button, 1, 1)

        self.confirm_button = QPushButton("Confirm Changes")
        self.layout.addWidget(self.confirm_button, 2, 0)

        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, 2, 1)

        # Abort button