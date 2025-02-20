from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CommandButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.buttons = []

        self.font = QFont("Arial", 16)

        self.create_layout()
        self.add_buttons()

    def create_layout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_buttons(self):
        self.queue_label = QLabel("Transmit Queue: 0")
        self.layout.addWidget(self.queue_label, 0, 0)

        button_names = ["Upload Waypoints", "Calibrate Gyroscopes", "Calibrate Accelerometers", "Next Waypoint"]
        for row in range(2):
            for col in range(2):
                button = QPushButton(button_names[row*2+col])
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setFont(self.font)
                self.layout.addWidget(button, 1+row, col)
                self.buttons.append(button)
    
    def update(self, transmit_queue_len):
        self.queue_label.setText("Transmit Queue: " + str(transmit_queue_len))