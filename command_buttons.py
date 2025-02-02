from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CommandButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.font = QFont("Arial", 16)

        self.create_layout()
        self.add_buttons()

    def create_layout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_buttons(self):
        self.queue_label = QLabel("Transmit Queue: 0")
        self.layout.addWidget(self.queue_label, 0, 0)

        self.return_button = QPushButton("Return to Home")
        self.return_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.return_button.setFont(self.font)
        self.layout.addWidget(self.return_button, 1, 0)

        self.calibrate_button = QPushButton("Calibrate Gyroscopes")
        self.calibrate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calibrate_button.setFont(self.font)
        self.layout.addWidget(self.calibrate_button, 1, 1)

        self.confirm_button = QPushButton("Confirm Changes")
        self.confirm_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.confirm_button.setFont(self.font)
        self.layout.addWidget(self.confirm_button, 2, 0)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancel_button.setFont(self.font)
        self.layout.addWidget(self.cancel_button, 2, 1)
    
    def update(self, transmit_queue_len):
        self.queue_label.setText("Transmit Queue: " + str(transmit_queue_len))