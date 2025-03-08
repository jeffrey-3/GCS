from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ParamsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))
        self.params_file_label = QLineEdit()
        self.params_file_label.setFixedWidth(500)
        self.params_btn = QPushButton("Import Parameters")
        formlayout = QFormLayout()
        formlayout.addRow(self.params_file_label, self.params_btn)
        self.layout.addLayout(formlayout)
        self.setLayout(self.layout)