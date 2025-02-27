from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class RawData(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)
    
    def update(self, queue_len):
        self.label.setText("Queue: " + str(queue_len))